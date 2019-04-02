#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 批量生成上海标答数据
import os
import urllib2
import json

kts_url = "http://10.11.5.43:13300"
kds_url = "http://10.11.5.43:23210"
kds_osis_url = "http://10.11.5.43:13230"
ref_kds_osis_url = "http://10.11.5.40:13230"


def getFusionData(taskId, i, dataType="lane"):
    url = "%s/kds-data/data/taskId/%s/fusion/query" % (kds_url, taskId)
    cmd = "wget %s -O ./%s/%s.json" % (url, str(i), dataType)
    os.system(cmd)


def getShape(taskId, output_path, isRef, dataType="lane"):
    url = "%s/kds-osis/shp/os/task/%s/fusion" % (kds_osis_url, taskId)
    refUrl = "%s/kds-osis/shp/os/task/%s/fusion" % (ref_kds_osis_url, taskId)

    if isRef:
        os.system("wget %s -O %s/refTask.zip" % (refUrl, output_path))
    else:
        os.system("wget %s -O %s/%sTask.zip" % (url, output_path, dataType))


def getFusionTaskInfoByProjecId(projectId, frameId2TaskId, fusionTaskId2OtherTaskId):
    url = "%s/kts/project/findTaskByProjectIdAndBussTypeAndFinished?projectId=%s&bussType=43" % (
        kts_url, projectId)
    response = urllib2.urlopen(url, timeout=10)
    jsonData = json.loads(response.read())
    results = jsonData["result"]
    for result in results:
        fusionTaskId = result["id"]
        tags = result["tags"]
        for tag in tags:
            if tag["k"] == "taskFrameId":
                frameId = tag["v"]
        frameId2TaskId[frameId] = fusionTaskId

        ground_url = "%s/kts/task/findTopology?taskId=%s&bussCode=groundFusion" % (kts_url, fusionTaskId)
        ground_json = json.loads(urllib2.urlopen(ground_url, timeout=10).read())
        groundTaskId = ground_json["result"][0]["id"]

        polesign_url = "%s/kts/task/findTopology?taskId=%s&bussCode=poleSignFusion" % (
            kts_url, fusionTaskId)
        polesign_json = json.loads(urllib2.urlopen(polesign_url, timeout=10).read())
        poleSignTaskId = polesign_json["result"][0]["id"]
        fusionTaskId2OtherTaskId[fusionTaskId] = (groundTaskId, poleSignTaskId)


# 记录任务框id与组网相关任务id的对应关系
def saveFrameId2TaskIds(output_path, frameId2RefTaskId, frameId2TaskId, fusionTaskId2OtherTaskId):
    with open(output_path, "w") as fp:
        fp.write("frameId,refTaskId,laneTaskId,groundTaskId,poleSignTaskId\n")
        for frameId in frameId2RefTaskId.keys():
            refTaskId = frameId2RefTaskId[frameId]
            laneTaskId = ""
            if frameId in frameId2TaskId.keys():
                laneTaskId = frameId2TaskId[frameId]
            #
            groundTaskId = ""
            poleSignTaskId = ""
            if laneTaskId in fusionTaskId2OtherTaskId.keys():
                (groundTaskId, poleSignTaskId) = fusionTaskId2OtherTaskId[laneTaskId]

            fp.write("%s,%s,%s,%s,%s\n" % (frameId, refTaskId, laneTaskId, groundTaskId, poleSignTaskId))


# 从all_task_info.csv中还原映射关系
def loadTaskInfos(input_path, frameId2RefTaskId, frameId2TaskId, fusionTaskId2OtherTaskId):
    with open(input_path) as fp:
        lines = fp.readlines()
        for line in lines[1:]:
            all = line.split(',')
            frameId = all[0]
            if frameId == "":
                continue
            refTaskId = all[1]
            laneTaskId = all[2]
            groundTaskId = all[3]
            poleSignTaskId = all[4][:-1]

            if refTaskId != "":
                frameId2RefTaskId[frameId] = refTaskId

            if laneTaskId != "":
                frameId2TaskId[frameId] = laneTaskId

            if groundTaskId != "" and poleSignTaskId != "":
                fusionTaskId2OtherTaskId[laneTaskId] = (groundTaskId, poleSignTaskId)


def saveMissingFusionTaskId(output_path, misingFusionTaskIdOfFrameId):
    with open(output_path, "w") as fp:
        for frameId in misingFusionTaskIdOfFrameId:
            fp.write(frameId + "\n")


if __name__ == '__main__':
    projectId = "1806"
    # path = '/Users/weihainan/Documents/automap2.0/input_shanghai'
    path = '/data1/coco/data/input_shanghai'
    # output_path = '/Users/weihainan/Documents/automap2.0/shanghai'
    output_path = '/data1/coco/data/shanghai'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 以frame_id命名文件夹
    frameId2RefTaskId = {}
    frameId2TaskId = {}
    fusionTaskId2OtherTaskId = {}
    all_task_info_path = output_path + "/all_task_info.csv"
    if not os.path.exists(all_task_info_path):
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                fullpath = os.path.join(dirpath, file)
                refTaskId = file.split("_")[0]
                frameId = file[len(refTaskId) + 1: -5]
                frameId2RefTaskId[frameId] = refTaskId
        #
        getFusionTaskInfoByProjecId(projectId, frameId2TaskId, fusionTaskId2OtherTaskId)
        saveFrameId2TaskIds(all_task_info_path, frameId2RefTaskId, frameId2TaskId, fusionTaskId2OtherTaskId)
    else:
        loadTaskInfos(all_task_info_path, frameId2RefTaskId, frameId2TaskId, fusionTaskId2OtherTaskId)

    #
    # 没有找到标答任务框对应融合任务的id
    misingFusionTaskIdOfFrameId = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            refTaskId = file.split("_")[0]
            frameId = file[len(refTaskId) + 1: -5]
            #
            os.chdir(output_path)
            os.system("mkdir " + frameId)
            os.system("cp " + fullpath + " " + frameId + "/refTask.json")
            with open(frameId + "/taskInfo.txt", "w") as fp:
                fp.write("refTaskId:%s\n" % refTaskId)
                getShape(refTaskId, frameId, True)

                fusionTaskId = ""
                if frameId in frameId2TaskId.keys():
                    fusionTaskId = frameId2TaskId[frameId]
                    fp.write("taskId:%s\n" % fusionTaskId)
                else:
                    print "fusionTaskId of %s frame is missing" % frameId
                    fp.write("taskId:missing\n")
                    misingFusionTaskIdOfFrameId.append(frameId)

                if fusionTaskId != "":
                    groundTaskId = fusionTaskId2OtherTaskId[fusionTaskId][0]
                    poleSignTaskId = fusionTaskId2OtherTaskId[fusionTaskId][1]

                    fp.write("groundTaskId:%s\n" % groundTaskId)
                    fp.write("poleSignTaskId:%s\n" % poleSignTaskId)

                    getShape(fusionTaskId, frameId, False, "lane")
                    getShape(groundTaskId, frameId, False, "ground")
                    getShape(poleSignTaskId, frameId, False, "poleSign")
                    getFusionData(fusionTaskId, frameId, "lane")
                    getFusionData(groundTaskId, frameId, "ground")
                    getFusionData(poleSignTaskId, frameId, "poleSign")
                else:
                    fp.write("groundTaskId:missing\n")
                    fp.write("poleSignTaskId:missing\n")

    misingFusionTaskIdOfFrameId_outputpath = output_path + "/misingFusionTaskIdOfFrameIdInfo.csv"
    saveMissingFusionTaskId(misingFusionTaskIdOfFrameId_outputpath, misingFusionTaskIdOfFrameId)

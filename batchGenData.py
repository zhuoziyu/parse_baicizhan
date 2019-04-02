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

def getShape(taskId, i, isRef, dataType="lane"):
    url = "%s/kds-osis/shp/os/task/%s/fusion" % (kds_osis_url, taskId)
    refUrl = "%s/kds-osis/shp/os/task/%s/fusion" % (ref_kds_osis_url, taskId)
    # response = urllib2.urlopen(url, timeout=10)
    if isRef:
        os.system("wget " + refUrl + " -O ./" + str(i) + "/refTask.zip")
    else:
        os.system("wget " + url + " -O ./" + str(i) + "/" + dataType + "Task.zip")


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


if __name__ == '__main__':
    projectId = "1806"
    path = '/Users/weihainan/Documents/automap2.0/input_shanghai'
    # path = '/data1/coco/data/input_shanghai'
    output_path = '/Users/weihainan/Documents/automap2.0/shanghai'
    # output_path = '/data1/coco/data/shanghai'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    i = 1
    refFrameId2TaskId = {}
    refFrameId2DirId = {}
    frameId2TaskId = {}
    fusionTaskId2OtherTaskId = {}
    getFusionTaskInfoByProjecId(projectId, frameId2TaskId, fusionTaskId2OtherTaskId)
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            refTaskId = file.split("_")[0]
            frameId = file[len(refTaskId) + 1: -5]
            refFrameId2TaskId[frameId] = refTaskId
            refFrameId2TaskId[frameId] = i
            print fullpath

            os.chdir(output_path)
            os.system("mkdir " + str(i))
            os.system("cp " + fullpath + " " + str(i) + "/refTask.json")
            with open(str(i) + "/taskInfo.txt", "w") as fp:
                fp.write(refTaskId)
            getShape(refTaskId, i, True)

            fusionTaskId = ""
            if frameId in frameId2TaskId.keys():
                fusionTaskId = frameId2TaskId[frameId]
            else :
                print "%s frame missing" % frameId

            if fusionTaskId != "":
                groundTaskId = fusionTaskId2OtherTaskId[fusionTaskId][0]
                poleSignTaskId = fusionTaskId2OtherTaskId[fusionTaskId][1]
                with open(str(i) + "/taskInfo.txt", "a+") as fp:
                    fp.write(str(fusionTaskId)+"\n")
                    fp.write(str(groundTaskId)+"\n")
                    fp.write(str(poleSignTaskId)+"\n")
                getShape(fusionTaskId, i, False, "lane")
                getShape(groundTaskId, i, False, "ground")
                getShape(poleSignTaskId, i, False, "poleSign")
                getFusionData(fusionTaskId, i, "lane")
                getFusionData(groundTaskId, i, "ground")
                getFusionData(poleSignTaskId, i, "poleSign")
            i += 1

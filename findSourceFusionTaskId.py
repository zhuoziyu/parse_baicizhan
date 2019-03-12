#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 查找对应融合任务的来源融合任务id
import os
import urllib2
import json


def getSourceTaskId(inputJson):
    jsonData = json.loads(inputJson)
    tags = jsonData["result"]["tags"]
    for tag in tags:
        if tag["k"] == "multiSourceBatchs":
            sourceTaskId = tag["v"]
            # 下划线的位置
            label_pos = sourceTaskId.find('_')
            sourceTaskId = sourceTaskId[:label_pos]
            return sourceTaskId


def findSourceTaskId(taskId):
    url = "http://10.11.5.38:13300/kts/task/findById?id=" + taskId
    response = urllib2.urlopen(url, timeout=10)
    return getSourceTaskId(response.read())


def getShape(taskId, i, isRef):
    url = "http://10.11.5.40:13230/kds-osis/shp/os/task/%s/fusion" % taskId
    # response = urllib2.urlopen(url, timeout=10)
    if isRef:
        os.system("wget " + url + " -O ./" + str(i) + "/refTask.zip")
    else:
        os.system("wget " + url + " -O ./" + str(i) + "/Task.zip")


with open("/Users/weihainan/Documents/automap2.0/taskIds.txt") as fp:
    i = 1
    for taskId in fp.readlines():
        realTaskId = taskId[:-1]
        sourceTaskId = findSourceTaskId(realTaskId)
        print realTaskId + ":" + sourceTaskId

        outputDir = "./" + str(i)
        os.system("mkdir " + outputDir)
        with open("./" + str(i) + "/taskInfo.txt", "w") as fp_w:
            fp_w.write(realTaskId+"\n")
            fp_w.write(sourceTaskId)

        getShape(realTaskId, i, True)
        getShape(sourceTaskId, i, False)
        i += 1

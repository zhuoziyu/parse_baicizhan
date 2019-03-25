#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 批量下载融合成果数据
import os
import urllib2
import json

def getFusionResult(taskId, i, isRef):
    url = "http://10.11.5.33:23210/kds-data/data/taskId/%s/fusion/query" % taskId
    # response = urllib2.urlopen(url, timeout=10)
    if isRef:
        os.system("wget " + url + " -O ./" + str(i) + "/refTask.json")
    else:
        os.system("wget " + url + " -O ./" + str(i) + "/task.json")

def getRefAndTaskId(taskInfoFilePath):
    with open(taskInfoFilePath) as fp:
        lines = fp.readlines()
        refTaskId = lines[0][:-1]
        taskId = lines[1]
        return (refTaskId, taskId)

path = '/Users/weihainan/Documents/automap2.0/diff'
for dirpath, dirnames, filenames in os.walk(path):
    for file in filenames:
        fullpath = os.path.join(dirpath, file)
        if fullpath.find("taskInfo.txt")!=-1:
            (refTaskId, taskId) = getRefAndTaskId(fullpath)
            print refTaskId, taskId
            #
            work_dir = dirpath.split('/')[-1]
            getFusionResult(refTaskId, work_dir, True)
            getFusionResult(taskId, work_dir, False)



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 批量执行融合差分程序
import os
import urllib2
import json

param = "krs_urls=http://10.11.5.34:13100/krs/ krms_urls=http://10.11.5.40:14100/krms/ kds_urls=http://10.11.5.32:23210/kds-data/ is_parallel_computing=true is_diff_by_task_id=true"

def getRefAndTaskId(taskInfoFilePath):
    with open(taskInfoFilePath) as fp:
        lines = fp.readlines()
        refTaskId = lines[0][:-1]
        taskId = lines[1]
        return (refTaskId, taskId)

def genDiffCliCmd(refTaskId, taskId, work_dir):
    res = "./autohdmap_multi_merge_diff_cli %s taskId=%s refTaskId=%s work_dir=%s" %(param, taskId, refTaskId, work_dir)
    return res

path = '/Users/weihainan/Documents/automap2.0/diff'
for dirpath, dirnames, filenames in os.walk(path):
    for file in filenames:
        fullpath = os.path.join(dirpath, file)
        if fullpath.find("taskInfo.txt")!=-1:
            (refTaskId, taskId) = getRefAndTaskId(fullpath)
            print refTaskId, taskId

            work_dir = dirpath.split('/')[-1]
            diffCliCmd = genDiffCliCmd(refTaskId, taskId, work_dir)
            print diffCliCmd
            os.chdir(path)
            os.system(diffCliCmd)


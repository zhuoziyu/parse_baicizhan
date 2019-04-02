#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 批量执行融合差分程序, 使用预下载好的融合结果跑
import os
import urllib2
import json
import time

import datetime


def time_differ(date1='12:55:05', date2='13:15:05'):
    '''
    @传入是时间格式如'12:55:05'
    '''
    date1 = datetime.datetime.strptime(date1, "%H:%M:%S")
    date2 = datetime.datetime.strptime(date2, "%H:%M:%S")
    if date1 < date2:
        return date2 - date1
    else:
        return date1 - date2


param = "krs_urls=http://10.11.5.34:13100/krs/ krms_urls=http://10.11.5.40:14100/krms/ kds_urls=http://10.11.5.32:23210/kds-data/ is_parallel_computing=true is_diff_by_task_id=false"


def getRefAndTaskId(taskInfoFilePath):
    with open(taskInfoFilePath) as fp:
        lines = fp.readlines()
        refTaskId = lines[0][:-1]
        taskId = lines[1]
        return (refTaskId, taskId)


def genDiffCliCmd(refTaskId, taskId, work_dir):
    res = "./autohdmap_multi_merge_diff_cli %s taskId=%s refTaskId=%s work_dir=%s" % (param, "1", "2", work_dir)
    return res


def runDiff(path, begin_num, end_num):
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            if fullpath.find("taskInfo.txt") != -1:
                # (refTaskId, taskId) = getRefAndTaskId(fullpath)
                # print refTaskId, taskId
                dir_num = int(dirpath[dirpath.rfind('/') + 1:])
                if dir_num >= begin_num and dir_num <= end_num:
                    work_dir = dirpath.split('/')[-1]
                    diffCliCmd = genDiffCliCmd("1", "2", work_dir)
                    print diffCliCmd
                    os.chdir(path)
                    os.system(diffCliCmd)


def runReport(path, begin_num, end_num, report_path):
    total_dividers = 0
    total_right_dividers = 0
    total_lost_dividers = 0
    total_shape_diff_dividers = 0
    total_redundance_dividers = 0
    total_prop_diff_dividers = 0
    total_da_diff_dividers = 0

    total_groundsymbols = 0
    total_right_groundsymbols = 0
    total_lost_groundsymbols = 0
    total_shape_diff_groundsymbols = 0
    total_redundance_groundsymbols = 0
    total_prop_diff_groundsymbols = 0

    total_poles = 0
    total_right_poles = 0
    total_lost_poles = 0
    total_redundance_poles = 0
    total_prop_diff_poles = 0

    total_trafficsigns = 0
    total_right_trafficsigns = 0
    total_lost_trafficsigns = 0
    total_shape_diff_trafficsigns = 0
    total_redundance_diff_trafficsigns = 0
    total_self_redundance_diff_trafficsigns = 0
    total_prop_diff_trafficsigns = 0

    with open(report_path, "w") as fp_w:
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                fullpath = os.path.join(dirpath, file)
                if fullpath.find("diff_report") != -1:
                    dir_num = int(dirpath[dirpath.rfind('/') + 1:])
                    if dir_num < begin_num or dir_num > end_num:
                        continue
                    with open(fullpath) as fp:
                        lines = fp.readlines()
                        divider_report = lines[1].split(',')
                        total_dividers += long(divider_report[0])
                        total_right_dividers += long(divider_report[1])
                        total_lost_dividers += long(divider_report[2])
                        total_shape_diff_dividers += long(divider_report[3])
                        total_redundance_dividers += long(divider_report[4])
                        total_prop_diff_dividers += long(divider_report[5])
                        total_da_diff_dividers += long(divider_report[6])

                        groundsymbol_report = lines[3].split(',')
                        total_groundsymbols += long(groundsymbol_report[0])
                        total_right_groundsymbols += long(groundsymbol_report[1])
                        total_lost_groundsymbols += long(groundsymbol_report[2])
                        total_shape_diff_groundsymbols += long(groundsymbol_report[3])
                        total_redundance_groundsymbols += long(groundsymbol_report[4])
                        total_prop_diff_groundsymbols += long(groundsymbol_report[5])

                        pole_report = lines[5].split(',')
                        total_poles += long(pole_report[0])
                        total_right_poles += long(pole_report[1])
                        total_lost_poles += long(pole_report[2])
                        total_redundance_poles += long(pole_report[3])
                        total_prop_diff_poles += long(pole_report[4])

                        trafficsign_report = lines[7].split(',')
                        total_trafficsigns += long(trafficsign_report[0])
                        total_right_trafficsigns += long(trafficsign_report[1])
                        total_lost_trafficsigns += long(trafficsign_report[2])
                        total_shape_diff_trafficsigns += long(trafficsign_report[3])
                        total_redundance_diff_trafficsigns += long(trafficsign_report[4])
                        total_self_redundance_diff_trafficsigns += long(trafficsign_report[5])
                        total_prop_diff_trafficsigns += long(trafficsign_report[6])

        fp_w.write("车道线总数,正确个数,丢失个数,形状错误个数,多召回个数,属性错误个数,da错误个数,正确率\n")
        if total_shape_diff_dividers == 0:
            fp_w.write("0,0,0,0,0,0,0,0\n")
        else:
            divider_right_percent = 1.0 * total_right_dividers / total_dividers
            fp_w.write("%d,%d,%d,%d,%d,%d,%d,%f\n" % (
                total_dividers, total_right_dividers, total_lost_dividers, total_shape_diff_dividers,
                total_redundance_dividers,
                total_prop_diff_dividers, total_da_diff_dividers, divider_right_percent))

        fp_w.write("地面定位目标总数,正确个数,丢失个数,形状错误个数,多召回个数,属性错误,正确率\n")
        if total_groundsymbols == 0:
            fp_w.write("0,0,0,0,0,0,0\n")
        else:
            groundsymbol_right_percent = 1.0 * total_right_groundsymbols / total_groundsymbols
            fp_w.write("%d,%d,%d,%d,%d,%d,%f\n" % (
                total_groundsymbols, total_right_groundsymbols, total_lost_groundsymbols,
                total_shape_diff_groundsymbols,
                total_redundance_groundsymbols, total_prop_diff_groundsymbols, groundsymbol_right_percent))

        fp_w.write("灯杆总数,正确个数,丢失个数,多召回个数,属性错误,正确率\n")
        if total_poles == 0:
            fp_w.write("0,0,0,0,0,0\n")
        else:
            pole_right_percent = 1.0 * total_right_poles / total_poles
            fp_w.write("%d,%d,%d,%d,%d,%f\n" % (
                total_poles, total_right_poles, total_lost_poles, total_redundance_poles, total_prop_diff_poles,
                pole_right_percent))

        fp_w.write("路牌总数,正确个数,丢失个数,形状错误个数,多召回个数,自身重复个数,属性错误,正确率\n")
        if total_trafficsigns == 0:
            fp_w.write("0,0,0,0,0,0,0,0\n")
        else:
            trafficsign_right_percent = 1.0 * total_right_trafficsigns / total_trafficsigns
            fp_w.write("%d,%d,%d,%d,%d,%d,%d,%f\n" % (
                total_trafficsigns, total_right_trafficsigns, total_lost_trafficsigns, total_shape_diff_trafficsigns,
                total_redundance_diff_trafficsigns, total_self_redundance_diff_trafficsigns,
                total_prop_diff_trafficsigns,
                trafficsign_right_percent))


if __name__ == '__main__':
    start = datetime.datetime.now()
    path = '/data1/coco/data/shanghai'
    # path = '/Users/weihainan/Documents/automap2.0/shanghai'
    report_path = '%s/total_report.csv' % path
    begin = 1
    end = 30
    runDiff(path, begin, end)
    runReport(path, begin, end, report_path)
    end = datetime.datetime.now()
    total_seconds = (end - start).total_seconds()
    used_hour = int(total_seconds / 3600.0)
    used_minitues = int((total_seconds - used_hour * 3600) / 60.0)
    used_seconds = int(total_seconds - used_hour * 3600 - used_minitues * 60)
    with open("time_used.txt", "w") as fp:
        fp.write("used time: %s hours, %s minitues, %s seconds " % (used_hour, used_minitues, used_seconds))

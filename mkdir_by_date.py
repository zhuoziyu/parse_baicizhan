#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 用于整理宝宝照片和视频,支持按照照片和视频的日期进行整理
import os

#将1.JPG或1.MOV文件夹中的文件移到根目录
def mvPicFromDir():
    pass

if __name__ == '__main__':
    path = 'f:/宝宝'
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)



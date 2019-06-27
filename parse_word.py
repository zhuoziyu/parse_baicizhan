#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 从本地百词斩单词中解析并输出到一个文件中，方便背诵
import os, json, codecs


def parse_single_word(word):
    jsonData = json.loads(word)
    word = jsonData["word"]
    accent = ""
    if "accent" in jsonData.keys():
        accent = jsonData["accent"]
    mean_cn = jsonData["mean_cn"]
    mean_en = ""
    if "mean_en" in jsonData.keys():
        mean_en = jsonData["mean_en"]
    sentence = jsonData["sentence"]
    sentence_trans = jsonData["sentence_trans"]
    return "%s;%s;%s;%s;%s,%s\n" % (word, accent, mean_cn, mean_en, sentence, sentence_trans)


def parse_word(path):
    with codecs.open("all_words.txt", "a+", "utf-8-sig") as fp_w:
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                fullpath = os.path.join(dirpath, file)
                # print fullpath
                if fullpath.find("meta.json") != -1:
                    fp = open(fullpath)
                    word = fp.readline()
                    fp_w.write(parse_single_word(word))


if __name__ == '__main__':
    parse_word("/Users/weihainan/Documents/github/baicizhan_zpk/extra_zpk")


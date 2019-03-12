#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 按照词根分类all_words

def category(words, categorys):
    # 每个单词是否分类过
    is_processed = [0] * len(words)
    for category in categorys:
        output_path = "./category/%s.txt" % category
        with open(output_path, "w") as fp:
            index = 0
            for word in words:
                index += 1
                word_eng = word.split(";")[0]
                if word_eng.find(category) != -1:
                    fp.write(word)
                    is_processed[index - 1] = 1

    with open("uncategory.txt", "w") as fp_uncategory:
        index = 0
        for word in words:
            if is_processed[index] == 0:
                fp_uncategory.write(word)
            #
            index += 1


if __name__ == '__main__':
    with open("all_words.txt") as fp:
        words = fp.readlines()
        with open("root.txt") as fp_root:
            categorys = []
            for line in fp_root.readlines():
                categorys.append(line[:-1])
            category(words, categorys)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 按照词根分类all_words

def category(words, categorys):
    for category in categorys:
        with open(category+".txt", "w") as fp:
            for word in words:
                word_eng = word.split(";")[0]
                if word_eng.find(category)!=-1:
                    fp.write(word)


if __name__ == '__main__':
    with open("all_words.txt") as fp:
        words = fp.readlines()
        categorys = ["fort", "dine", "tary", "fied", "dian", "table", "ceive", "dish", "try", "jack", "aint", "ppy", "ate", "dence", "tive", "eak", "ume", "lace", "oir"]
        category(words, categorys)



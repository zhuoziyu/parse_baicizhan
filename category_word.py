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
        # categorys = ["fort", "dine", "tary", "fied", "dian", "table", "ceive", "dish", "try", "jack", "aint", "ppy",
        #              "ate", "dence", "tive", "eak", "ume", "lace", "oir", "ise", "tion", "obe", "ble", "ain", "ent", "ght", "ace", "lut", "ice", "orn", "ide", "sly", "phe", "ous", "eer", "use", "out", "ing", "shed", "ait", "der", "ime", "ness", "sion", "eign", "ould", "ass", "edge", "ter", "lar", "ear", "ump", "acid", "acri", "acrid", "acu", "act", "aer", "aero", "aeri", "ag", "agri", "agro", "agr", "alter", "altern", "ali", "am", "amor", "amat", "ambul", "anim", "ann", "enn", "aqu", "arch", "archy", "art", "audi", "audit", "av", "avar", "avi", "ball", "bol", "bas", "base", "bell", "bel", "brev", "cad", "cas", "cid", "cand", "cant", "cent", "cap", "capt", "cept", "ceive", "cip", "cup", "card", "cord", "ced", "ceed", "cess", "celer", "centr", "cern", "cert", "cret", "chron", "cid", "cis", "cit", "claim", "clam", "clin", "cliv", "clos", "clud", "clus", "corp", "corpor", "creed", "cred", "cre", "creas", "cruc", "crus", "crux", "crpt", "cub", "cumb", "cur", "dent", "derm", "dermat", "dict", "dic", "dign", "doc", "don", "dit", "dur", "dyn", "dynam", "em", "empt", "ampl", "equ", "equi", "erg", "err", "ev", "fabl", "fabul", "fac", "fic", "fac", "fact", "fect", "fic", "fig", "fail", "fall", "fault", "fer", "ferv", "fid", "fin", "flam", "flagr", "flect", "flex", "flict", "flor", "flour", "flu", "fore", "fort", "form", "fract", "frang", "frig", "friger", "fug", "fus", "gen", "gener", "genit", "gnos", "gnor", "gon", "grad", "grat", "gree", "grav", "griev", "greg", "gress", "habit", "hap", "her", "hes", "hibit", "hydy", "hydro", "idea", "ideo", "ject", "judg", "judic", "jur", "juris", "labor", "laps", "lav", "luv", "lut", "lect", "lig", "leg", "legis", "lev", "live", "loc", "lingu"]
            category(words, categorys)

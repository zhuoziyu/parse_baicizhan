#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,  codecs

def gen_render_xml(data_path):
    mesh_code = data_path.split("/")[-2]
    # print mesh_code
    render_xml = '''<Layer name="%s" srs="+proj=latlong +ellps=WGS84 +datum=WGS84 +no_defs" maxzoom="750000" status="1">
    <StyleName>WRoads6_1</StyleName>
    <StyleName>WRoads6_2</StyleName>
    <Datasource>
        <Parameter name="type">shape</Parameter>
        <Parameter name="file">%s</Parameter>
    </Datasource>
</Layer>''' % (mesh_code, data_path)
    print render_xml

def parse_word(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            if fullpath.find(".shp")!=-1:
                # print fullpath
                gen_render_xml(fullpath)
if __name__ == '__main__':
    parse_word("/Users/weihainan/Downloads/chongqing")

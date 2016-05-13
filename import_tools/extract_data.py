#!/usr/bin/env python
# coding=utf-8

import config as cfg
import zipfile
import MySQLdb
import os



def find_zip(filename):

    pass

def open_inpx():
    print "parse inpx file"
    inpx = zipfile.ZipFile(cfg.LIBRARY["inpx_file"], 'r')
    list_of_inps = inpx.infolist()
    for inp in list_of_inps:
        if inp.filename.startswith("fb2"):
            doc = inpx.read(inp.filename)
            lines = doc.splitlines()
            for line in lines:
                print line




def start_process():
    open_inpx()


if __name__ == "__main__":
    start_process()
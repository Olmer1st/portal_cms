#!/usr/bin/env python
# coding=utf-8

import config as cfg
import zipfile
import MySQLdb
import os
import boo

def create_folder(filename):
    pass


def find_zip(filename):
    pass


def parse_inpx(inpx):
    print "parse inpx file"
    infolist = inpx.infolist()
    for inp in infolist:
        if inp.filename.startswith("fb2"):
            doc = inpx.read(inp.filename)
            lines = doc.splitlines()
            for line in lines:
                print line


def open_inpx():
    print "open inpx file"
    inpx = zipfile.ZipFile(cfg.LIBRARY["inpx_file"], 'r')




def start_process():
    inpx = open_inpx()
    parse_inpx(inpx)


if __name__ == "__main__":
    start_process()
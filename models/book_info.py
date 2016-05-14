#!/usr/bin/env python
# coding=utf-8

import config as cfg


"""AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;KEYWORDS"""


class BookInfo(object):

    def __init__(self):
        self._author = None
        self._genre = None
        self._title = None
        self._series = None
        self._serno = None
        self._file = None
        self._size = None
        self._libid= None
        self._del= None
        self._ext= None
        self._date= None
        self._lang= None
        self._keywords= None


    def load_from_line(self, line):
        if line is None or len(line)==0:
            return
        tmp = line.split(chr(0x04))
        self._author = tmp[0]
        self._genre = tmp[1]
        self._author = tmp[2]
        self._series = tmp[3]
        self._serno = tmp[4]
        self._file = tmp[5]
        self._size = tmp[6]
        self._libid    = tmp[7]
        self._del = tmp[8]
        self._ext = tmp[9]
        self._date = tmp[10]
        self._lang = tmp[11]
        self._keywords = tmp[12]
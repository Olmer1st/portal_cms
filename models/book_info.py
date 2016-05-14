#!/usr/bin/env python
# coding=utf-8

import config as cfg


"""AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;KEYWORDS;<CR><LF>"""


class BookInfo(object):

    def __init__(self):
        self._author = None
        self._genre = None
        self._title = None
        self._series = None
        self._serno = None
        self._file = None
        self._size = None
        self.libid= None
        self._del= None
        self._ext= None
        self._date= None
        self._lang= None
        self._keywords= None


    def loadFromLine(self, line):
        if line is None or len(line)>0:
            pass
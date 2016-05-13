#!/usr/bin/env python
# coding=utf-8


"""AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;KEYWORDS;<CR><LF>"""


class BookInfo(object):

    mysql_connection = None

    def __init__(self, line=None):
        pass
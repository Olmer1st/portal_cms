#!/usr/bin/env python
# coding=utf-8

import config as cfg
import  book_info


"""AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;KEYWORDS;<CR><LF>"""


class Books(object):


    def __init__(self):
        self.mysql_connection = None
        pass

    def find_by_name(self):
        pass

    def find_by_bid(self):
        pass

    def find_by_file(self):
        pass
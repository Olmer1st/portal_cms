#!/usr/bin/env python
# coding=utf-8

import config as cfg

"""AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;LIBRATE;KEYWORDS;"""


class BookInfo(object):
    def __init__(self):
        self._author = None
        self._genre = None
        self._title = None
        self._series = None
        self._serno = None
        self._file = None
        self._size = None
        self._libid = None
        self._del = None
        self._ext = None
        self._date = None
        self._lang = None
        self._librate = None
        self._keywords = None
        self._path = None
        self._bid = None

    def load_from_line(self, line):
        if line is None or len(line) == 0:
            return

        tmp_arr = [field.decode('utf8') if len(field) > 0 else None for field in line.split(chr(0x04))]
        self._author = tmp_arr[0]
        self._genre = tmp_arr[1]
        self._title = tmp_arr[2]
        self._series = tmp_arr[3]
        self._serno = tmp_arr[4]
        self._file = tmp_arr[5]
        self._size = tmp_arr[6]
        self._libid = tmp_arr[7]
        self._del = tmp_arr[8]
        self._ext = tmp_arr[9]
        self._date = tmp_arr[10]
        self._lang = tmp_arr[11]
        self._librate = tmp_arr[12]
        self._keywords = tmp_arr[13]

    def load_from_row(self, row):
        if row is None:
            return
        self._author = row['AUTHOR']
        self._genre = row['GENRE']
        self._title = row['TITLE']
        self._series = row['SERIES']
        self._serno = row['SERNO']
        self._file = row['FILE']
        self._size = row['SIZE']
        self._libid = row['LIBID']
        self._del = row['DEL']
        self._ext = row['EXT']
        self._date = row['DATE']
        self._lang = row['LANG']
        self._librate = row['LIBRATE']
        self._keywords = row['KEYWORDS']
        self._path = row['PATH']
        self._bid = row['BID']

    def load_from_row_partial(self, row):
        if row is None:
            return
        self._bid = row[0]
        self._author = row[1]
        self._genre = row[2]
        self._series = row[3]
        self._serno = row[4]
        self._file = row[5]

    def set_path(self, path):
        self._path = path

    def set_bid(self, bid):
        self._bid = bid

    def file_name(self):
        if self._file is None and self._ext is None:
            return ""
        return "{0}.{1}".format(self._file, self._ext)

    def get_data(self):
        return (self._author, self._genre, self._title, self._series, self._serno, self._file, self._size,
                self._libid, self._del, self._ext, self._date, self._lang, self._librate, self._keywords, self._path)

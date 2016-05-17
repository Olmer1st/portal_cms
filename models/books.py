#!/usr/bin/env python
# coding=utf-8

import config as cfg
import book_info
import MySQLdb

"""AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;KEYWORDS;<CR><LF>"""


class Books(object):
    def __init__(self):
        self.db = MySQLdb.connect(cfg.DB["servername"], cfg.DB["username"], cfg.DB["password"], cfg.DB["dbname"],
                                  charset=cfg.DB["charset"])
        self.cursor = self.db.cursor()

    def find_by_author(self):
        pass

    def find_by_name(self):
        pass

    def find_by_bid(self, bid):
        info = None
        sql = u"SELECT AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,KEYWORDS,BID FROM {0} WHERE BID = {1}".format(
            cfg.DB["main_table"], bid)
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            info = book_info.BookInfo()
            info.load_from_row(row)

        except:
            print "Error: unable to fecth data"
        return info

    def find_by_file(self, libid, filename):
        info = None
        sql = u"SELECT AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,KEYWORDS,BID FROM {0} WHERE LIBID = {1} AND  FILE = {2}".format(
            cfg.DB["main_table"], libid, filename)
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            info = book_info.BookInfo()
            info.load_from_row(row)

        except:
            print "Error: unable to fecth data"
        return info

    def save_book(self, info):
        if info is None:
            return
        id = None
        sql = u"INSERT INTO {0}(AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,KEYWORDS) VALUES ('{1}','{2}','{3}','{4}',{5},{6},{7},{8},{9},'{10}','{11}','{12}','{13}')".format(
            cfg.DB["main_table"], info._author,
            info._genre, info._title,
            info._series if info._series is not None else '', info._serno if info._serno is not None else 'NULL',
            info._file, info._size, info._libid,
            info._del if info._del is not None else 'NULL', info._ext, info._date,
            info._lang, info._keywords if info._keywords is not None else '')

        try:
            self.cursor.execute(sql)
            self.db.commit()
            id = self.cursor.lastrowid
        except:
            self.db.rollback()
        return id

    def close(self):
        if self.db is not None:
            self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

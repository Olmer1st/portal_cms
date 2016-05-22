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
        sql = u"SELECT AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS,BID FROM {} WHERE BID = %s".format(
            cfg.DB["main_table"])

        try:
            self.cursor.execute(sql, (bid))
            row = self.cursor.fetchone()
            info = book_info.BookInfo()
            info.load_from_row(row)

        except:
            print "Error: unable to fecth data"
        return info

    def find_by_file(self, libid, filename):
        info = None
        sql = u"SELECT AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS,BID FROM {} WHERE LIBID = %s AND  FILE = %s".format(
            cfg.DB["main_table"])
        try:
            self.cursor.execute(sql, (int(libid), int(filename)))
            row = self.cursor.fetchone()
            info = book_info.BookInfo()
            info.load_from_row(row)

        except Exception as error:
            print "Error: unable to fecth data %s" % error
        return info

    def save_book(self, info):
        if info is None:
            return
        id = None
        sql = u"INSERT INTO {} (AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s ,%s)".format(
            cfg.DB["main_table"])

        try:
            self.cursor.execute(sql, info.get_data())
            self.db.commit()
            id = self.cursor.lastrowid
        except Exception as error:
            self.db.rollback()
        return id

    def update_book(self, info, bid):
        if info is None or bid is None:
            return
        sql = u"UPDATE {} SET DEL = %s,LIBRATE = %s, KEYWORDS = %s WHERE BID = %s".format(cfg.DB["main_table"])

        try:
            self.cursor.execute(sql, (info._del, info._librate, info._keywords, bid))
            self.db.commit()
        except Exception as error:
            # print(error)
            self.db.rollback()

    def close(self):
        try:
            if self.db is not None:
                if self.cursor is not None:
                    self.cursor.close()
                    del self.cursor
                self.db.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

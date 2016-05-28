#!/usr/bin/env python
# coding=utf-8

import config as cfg
import book_info
import MySQLdb

"""books_data: AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;LIBRATE;KEYWORDS;ETC
   inp_list: INP_ID, INP_NAME, INSERTED"""


class Books(object):
    def __init__(self):
        self.db = MySQLdb.connect(cfg.DB["servername"], cfg.DB["username"], cfg.DB["password"], cfg.DB["dbname"],
                                  charset=cfg.DB["charset"])
        self.cursor = self.db.cursor()

    def get_all_books(self):
        sql = u"SELECT BID, AUTHOR, GENRE,SERIES,SERNO,FILE FROM {0}".format(cfg.DB["main_table"])
        rows = None
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return rows

    def is_author_exist(self, author_name):
        sql = u"SELECT AID FROM {0} WHERE FULLNAME = '{1}'".format(cfg.DB["authors_table"], author_name)
        id = None
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is not None:
                id = row[0]

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return id

    def is_serie_exist(self, serie_name):
        sql = u"SELECT SID FROM {0} WHERE SERIE_NAME = '{1}'".format(cfg.DB["series_table"], serie_name)
        id = None
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is not None:
                id = row[0]

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return id

    def is_genre_exist(self, genre_name):
        sql = u"SELECT GID FROM {0} WHERE CODE = '{1}'".format(cfg.DB["genres_table"], genre_name)
        id = None
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is not None:
                id = row[0]

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return id

    def insert_author(self, author_name):
        id = None
        sql = u"INSERT INTO {0} (FULLNAME) VALUES('{1}')".format(cfg.DB["authors_table"], author_name)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            id = self.cursor.lastrowid
        except Exception as error:
            # print error
            self.db.rollback()
        return id

    def insert_author2book(self, aid, bid):
        sql = u"INSERT INTO {0} (AID, BID) VALUES({1}, {2})".format(cfg.DB["author2book"], aid, bid)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as error:
            # print error
            self.db.rollback()

    def insert_serie(self, serie_name):
        id = None
        sql = u"INSERT INTO {0} (serie_name) VALUES('{1}')".format(cfg.DB["series_table"], serie_name)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            id = self.cursor.lastrowid
        except Exception as error:
            # print error
            self.db.rollback()
        return id

    def insert_serie2book(self, sid, bid, sn):
        sql = u"INSERT INTO {0} (SID, BID, SERIE_NUMBER) VALUES({1}, {2}, {3})".format(cfg.DB["serie2book"], sid, bid,
                                                                                       sn if sn is not None else 'NULL')
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as error:
            # print error
            self.db.rollback()

    def insert_genre2book(self, gid, bid):
        sql = u"INSERT INTO {0} (GID, BID) VALUES({1}, {2})".format(cfg.DB["genre2book"], gid, bid)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as error:
            # print error
            self.db.rollback()

    def get_authors_from_books(self):
        sql = "SELECT DISTINCT AUTHOR FROM {0}".format(cfg.DB["main_table"])
        rows = None
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return rows

    def find_by_author(self, aid):
        data = {
            'error': None,
            'rows': []
        }
        sql = u"SELECT * FROM {0} WHERE AID =  {1}".format(cfg.DB["booksByAuthor"], aid)

        try:
            self.cursor.execute(sql)
            data['rows'] = self.cursor.fetchall()
        except:
            data['error'] = "Error: unable to fecth data"
        return data

    def find_by_name(self):
        pass

    def is_inp_exist(self, name):
        sql = "SELECT INP_ID FROM {0} WHERE INP_NAME = '{1}' AND STATUS='1'".format(cfg.DB["inp_table"], name)
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is not None and row[0] is not None:
                return True

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return False

    def add_inp(self, name):
        id = None
        sql = "INSERT INTO {0} (INP_NAME) VALUES('{1}')".format(cfg.DB["inp_table"], name)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            id = self.cursor.lastrowid
        except Exception as error:
            # print error
            self.db.rollback()
        return id

    def update_inp(self, inp_id):
        if inp_id is None:
            return
        sql = "UPDATE {} SET STATUS=%s WHERE INP_ID=%s".format(cfg.DB["inp_table"])
        try:
            self.cursor.execute(sql, ('1', inp_id))
            self.db.commit()
        except Exception as error:
            # print error
            self.db.rollback()

    def find_by_bid(self, bid):
        info = None
        sql = u"SELECT AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS, PATH, BID FROM {} WHERE BID = %s".format(
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
        sql = u"SELECT AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS, PATH, BID FROM {} WHERE LIBID = %s AND  FILE = %s".format(
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
        sql = u"INSERT INTO {} (AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS,PATH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s ,%s,%s)".format(
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
        sql = u"UPDATE {} SET AUTHOR = %s, TITLE=%s, GENRE=%s, DEL = %s, LIBRATE = %s, KEYWORDS = %s, UPDATED = CURRENT_TIMESTAMP, PATH = %s WHERE BID = %s".format(
            cfg.DB["main_table"])

        try:
            self.cursor.execute(sql,
                                (info._author, info._title, info._genre, info._del, info._librate, info._keywords,
                                 info._path, bid))
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

#!/usr/bin/env python
# coding=utf-8

import config as cfg
import book_info
from middleware.dbconnection import mysql_connection

"""books_data: AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;LIBRATE;KEYWORDS;ETC
   inp_list: INP_ID, INP_NAME, INSERTED
   """


class Books(object):
    def __init__(self):
        self.connection = mysql_connection()

    def get_all_languages(self):
        sql = "SELECT * FROM {0} ORDER BY LANG".format(cfg.DB["allLanguages"])
        rows = None
        try:
            rows = self.connection.execute_fetch(sql, False)

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return rows

    def get_all_books(self):
        sql = u"SELECT BID, AUTHOR, GENRE,SERIES,SERNO,FILE FROM {0}".format(cfg.DB["main_table"])
        rows = None
        try:
            rows = self.connection.execute_fetch(sql, False)

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return rows

    def is_author_exist(self, author_name):
        sql = u"SELECT AID FROM {0} WHERE FULLNAME = '{1}'".format(cfg.DB["authors_table"], author_name)
        id = None
        try:
            row = self.connection.execute_fetch(sql)
            if row is not None:
                id = row['AID']

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return id

    def is_serie_exist(self, serie_name):
        sql = u"SELECT SID FROM {0} WHERE SERIE_NAME = '{1}'".format(cfg.DB["series_table"], serie_name)
        id = None
        try:
            row = self.connection.execute_fetch(sql)
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
            row = self.connection.execute_fetch(sql)
            if row is not None:
                id = row[0]

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return id

    def insert_author(self, author_name):

        sql = u"INSERT INTO {0} (FULLNAME) VALUES('{1}')".format(cfg.DB["authors_table"], author_name)
        return self.connection.execute_transact(sql)

    def insert_author2book(self, aid, bid):
        sql = u"INSERT INTO {0} (AID, BID) VALUES({1}, {2})".format(cfg.DB["author2book"], aid, bid)
        return self.connection.execute_transact(sql)

    def insert_serie(self, serie_name):
        sql = u"INSERT INTO {0} (serie_name) VALUES('{1}')".format(cfg.DB["series_table"], serie_name)
        return self.connection.execute_transact(sql)

    def insert_serie2book(self, sid, bid, sn):
        sql = u"INSERT INTO {0} (SID, BID, SERIE_NUMBER) VALUES({1}, {2}, {3})".format(cfg.DB["serie2book"], sid, bid,
                                                                                       sn)
        return self.connection.execute_transact(sql)

    def insert_genre2book(self, gid, bid):
        sql = u"INSERT INTO {0} (GID, BID) VALUES({1}, {2})".format(cfg.DB["genre2book"], gid, bid)
        return self.connection.execute_transact(sql)

    def get_authors_from_books(self):
        sql = "SELECT DISTINCT AUTHOR FROM {0}".format(cfg.DB["main_table"])
        rows = None
        try:
            rows = self.connection.execute_fetch(sql, False)
        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return rows

    def find_by_author(self, aid, lang='ru', hide=True):
        data = {
            'error': None,
            'rows': []
        }
        lang_part = ""
        hide_part = ""
        if lang != 'all':
            lang_part = " AND LANG = '{}'".format(lang)
        if hide:
            hide_part = " AND DEL IS NULL"
        sql = "SELECT * FROM {0} WHERE AID =  {1}".format(cfg.DB["booksByAuthor"], aid)
        sql = sql + lang_part + hide_part

        try:
            data['rows'] = self.connection.execute_fetch(sql, False)

        except:
            data['error'] = "Error: unable to fecth data"
        return data

    def find_by_name(self):
        pass

    def is_inp_exist(self, name):
        sql = "SELECT INP_ID FROM {0} WHERE INP_NAME = '{1}' AND STATUS='1'".format(cfg.DB["inp_table"], name)
        try:
            row = self.connection.execute_fetch(sql)
            return row is not None

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return False

    def add_inp(self, name):
        sql = "INSERT INTO {0} (INP_NAME) VALUES('{1}')".format(cfg.DB["inp_table"], name)
        return self.connection.execute_transact(sql)

    def update_inp(self, inp_id):
        if inp_id is None:
            return
        sql = "UPDATE {} SET STATUS=%s WHERE INP_ID=%s".format(cfg.DB["inp_table"])
        self.connection.execute_transact(sql, ('1', inp_id), True)

    def find_by_bid(self, bid):
        info = None
        sql = u"SELECT AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS, PATH, BID FROM {} WHERE BID = %s".format(
            cfg.DB["main_table"])

        try:
            row = self.connection.execute_fetch(sql, True, (bid))
            info = book_info.BookInfo()
            info.load_from_row(row)

        except:
            print "Error: unable to fetch data"
        return info

    def find_by_sid(self, sid, lang='ru', hide=True):
        data = {
            'error': None,
            'rows': []
        }
        lang_part = ""
        hide_part = ""
        if lang != 'all':
            lang_part = " AND LANG = '{}'".format(lang)

        if hide:
            hide_part = " AND DEL IS NULL"
        sql = "SELECT * FROM {0} WHERE SID = {1}".format(cfg.DB["booksBySerie"], sid)
        sql = sql + lang_part + hide_part
        try:
            data['rows'] = self.connection.execute_fetch(sql, False)
        except:
            data['error'] = "Error: unable to fetch data"
        return data

    def find_by_gid(self, gid, lang='ru', hide=True):
        data = {
            'error': None,
            'rows': []
        }
        # limit_part = " LIMIT {0},{1}".format(start, end)
        lang_part = ""
        hide_part = ""
        if lang != 'all':
            lang_part = " AND LANG = '{}'".format(lang)
        if hide:
            hide_part = " AND DEL IS NULL"
        sql = "SELECT * FROM {0} WHERE GID = {1}".format(cfg.DB["booksByGenre"], gid)
        sql = sql + lang_part + hide_part
        try:
            data['rows'] = self.connection.execute_fetch(sql, False)
        except:
            data['error'] = "Error: unable to fetch data"
        return data

    def find_by_gid_sp(self, gid, lang='ru', hide=True):
        data = {
            'error': None
        }

        result = self.connection.call_proc_fetch(cfg.DB['getAllDataByGenre'], (gid, lang, 0 if not hide else 1))
        data['books_no_serie'] = result[3] if len(result) > 0 else []
        data['books_by_serie'] = result[2] if len(result) > 0 else []
        data['authors'] = result[0] if len(result) > 1 else []
        data['series'] = result[1] if len(result) > 1 else []
        return data

    def find_by_search_sp(self, options, lang='ru', hide=True):
        """IN `author` VARCHAR(500) CHARSET utf8, IN `title` VARCHAR(500) CHARSET utf8, IN `iGid` INT, IN `fromDate` VARCHAR(20), IN `toDate` VARCHAR(20), IN `sLang` VARCHAR(10) CHARSET utf8, IN `iDel` INT"""
        data = {
            'error': None
        }

        result = self.connection.call_proc_fetch(cfg.DB['getAllDataBySearchParams'], (
        options['author'], options['title'], options['gid'], options['fromDate'], options['toDate'], lang,
        0 if not hide else 1))
        data['books_no_serie'] = result[3] if len(result) > 0 else []
        data['books_by_serie'] = result[2] if len(result) > 0 else []
        data['authors'] = result[0] if len(result) > 1 else []
        data['series'] = result[1] if len(result) > 1 else []
        return data

    def find_by_file(self, libid, filename):
        info = None
        sql = u"SELECT AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS, PATH, BID FROM {} WHERE LIBID = %s AND  FILE = %s".format(
            cfg.DB["main_table"])
        try:
            row = self.connection.execute_fetch(sql, True, (int(libid), int(filename)))
            info = book_info.BookInfo()
            info.load_from_row(row)

        except Exception as error:
            print "Error: unable to fecth data %s" % error
        return info

    def save_book(self, info):
        if info is None:
            return None
        sql = u"INSERT INTO {} (AUTHOR,GENRE,TITLE,SERIES,SERNO,FILE,SIZE,LIBID,DEL,EXT,DATE,LANG,LIBRATE,KEYWORDS,PATH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s ,%s,%s)".format(
            cfg.DB["main_table"])
        return self.connection.execute_transact(sql, info.get_data())

    def update_book(self, info, bid):
        if info is None or bid is None:
            return
        sql = u"UPDATE {} SET AUTHOR = %s, TITLE=%s, GENRE=%s, DEL = %s, LIBRATE = %s, KEYWORDS = %s, UPDATED = CURRENT_TIMESTAMP, PATH = %s WHERE BID = %s".format(
            cfg.DB["main_table"])
        self.connection.execute_transact(sql, (
            info._author, info._title, info._genre, info._del, info._librate, info._keywords,
            info._path, bid), True)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

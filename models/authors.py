#!/usr/bin/env python
# coding=utf-8

import config as cfg
import MySQLdb


class Authors(object):
    def __init__(self):
        self.db = MySQLdb.connect(cfg.DB["servername"], cfg.DB["username"], cfg.DB["password"], cfg.DB["dbname"],
                                  charset=cfg.DB["charset"])
        self.cursor = self.db.cursor()

    def is_author_exist(self, author_name):
        sql = u"SELECT AID FROM {0} WHERE FULLNAME = '{1}'".format(cfg.DB["authors_table"], author_name)
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            if row is not None and row[0] is not None:
                return True

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return False

    def find_by_fullname(self, search_str):
        data = {
            'error':None,
            'rows':[]
        }
        sql = u"SELECT AID, FULLNAME FROM {0} WHERE FULLNAME like '%{1}%'".format(cfg.DB["authors_table"], search_str)
        try:
            self.cursor.execute(sql)
            data['rows'] = self.cursor.fetchall()
        except Exception as error:
            data['error'] = error.message
        return data

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

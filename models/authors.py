#!/usr/bin/env python
# coding=utf-8

import config as cfg
from middleware.dbconnection import mysql_connection

"""`lib_authors`.`AID`, `lib_authors`.`FULLNAME`, `lib_authors`.`INSERTED`"""


class Authors(object):
    def __init__(self):
        self.connection = mysql_connection()

    def is_author_exist(self, author_name):
        sql = u"SELECT AID FROM {0} WHERE FULLNAME = '{1}'".format(cfg.DB["authors_table"], author_name)
        try:

            row = self.connection.execute_fetch(sql)
            return row is not None

        except Exception as error:
            pass
            # print "Error: unable to fecth data %s" % error

        return False

    def find_by_fullname(self, search_str):
        data = {
            'error': None,
            'rows': []
        }
        sql = u"SELECT AID, FULLNAME FROM {0} WHERE FULLNAME like '%{1}%'".format(cfg.DB["authors_table"], search_str)
        try:
            data['rows'] = self.connection.execute_fetch(sql,False)
        except Exception as error:
            data['error'] = error.message
        return data

    def find_by_ids(self, aids):
        str_list_of_aids = ",".join(aids)
        data = {
            'error': None,
            'rows': []
        }
        sql = u"SELECT AID, FULLNAME FROM {0} WHERE AID IN ({1})".format(cfg.DB["authors_table"], str_list_of_aids)
        try:
            data['rows'] = self.connection.execute_fetch(sql, False)
        except Exception as error:
            data['error'] = error.message
        return data

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

#!/usr/bin/env python
# coding=utf-8

import config as cfg
from middleware.dbconnection import mysql_connection

"""books_data: `view_seriesByBook`.`SID`, `view_seriesByBook`.`BID`, `view_seriesByBook`.`serie_name`, `view_seriesByBook`.`serie_number`"""


class Series(object):
    def __init__(self):
        self.connection = mysql_connection()

    def find_serie_by_book(self, bid):
        sql = u"SELECT SID,BID,SERIE_NAME,SERIE_NUMBER FROM {0} WHERE BID={1}".format(cfg.DB["seriesByBook"], bid)
        return self.connection.execute_fetch(sql)

    def find_series_by_books(self, books):
        str_list_of_books = ",".join(books)
        sql = u"SELECT SID,BID,SERIE_NAME,SERIE_NUMBER FROM {0} WHERE BID in ({1})".format(cfg.DB["seriesByBook"],
                                                                                           str_list_of_books)
        return self.connection.execute_fetch(sql)

    def get_all_series(self, start=1, end=50):
        sql = "SELECT COUNT(*) as 'totalSeries' FROM {0}".format(cfg.DB["series_table"])
        row = self.connection.execute_fetch(sql)
        sql = "SELECT * FROM {0} ORDER BY SERIE_NAME LIMIT {1},{2}".format(cfg.DB["AllSeries"], start, end)
        rows = self.connection.execute_fetch(sql, False)
        return {'totalSeries': row['totalSeries'], 'series':rows}

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

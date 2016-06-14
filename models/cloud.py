#!/usr/bin/env python
# coding=utf-8

import config as cfg
from middleware.dbconnection import mysql_connection


class Cloud(object):
    def __init__(self):
        self.connection = mysql_connection()

    def get_link_by_bid(self,bid):
        sql = "SELECT * FROM {0} WHERE BID ={1}".format(cfg.DB["cloud"], bid)
        row = self.connection.execute_fetch(sql)
        return row

    def save_link(self, bid, link_id, code):
        sql = "INSERT INTO {0} (bid,linkid, code) VALUES({1},{2},'{3}')".format(
            cfg.DB["cloud"], bid, link_id, code)
        return self.connection.execute_transact(sql)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

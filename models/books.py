#!/usr/bin/env python
# coding=utf-8

import config as cfg
import book_info
import MySQLdb

"""AUTHOR;GENRE;TITLE;SERIES;SERNO;FILE;SIZE;LIBID;DEL;EXT;DATE;LANG;KEYWORDS;<CR><LF>"""


class Books(object):
    def __init__(self):
        self.db = MySQLdb.connect(cfg.DB["servername"], cfg.DB["username"], cfg.DB["password"], cfg.DB["dbname"])
        self.cursor = self.db.cursor()

    def find_by_name(self):
        pass

    def find_by_bid(self):
        pass

    def find_by_file(self, libid, filename):
        pass

    def save_book(self, info):
        sql = sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
                LAST_NAME, AGE, SEX, INCOME) \
                VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
                ('Mac', 'Mohan', 20, 'M', 2000)

        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()

    def close(self):
        if self.db is not None:
            self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

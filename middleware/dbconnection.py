#!/usr/bin/env python
# coding=utf-8

import config as cfg
import MySQLdb
from MySQLdb import cursors


class mysql_connection:
    def __init__(self):
        self._db = MySQLdb.connect(host=cfg.DB["host"], port=cfg.DB["port"], user=cfg.DB["username"],
                                   passwd=cfg.DB["password"], db=cfg.DB["dbname"],
                                   charset=cfg.DB["charset"], cursorclass=cursors.DictCursor)
        self._cursor = self._db.cursor()

    @property
    def cursor(self):
        return self._cursor

    def execute_fetch(self, sql, one=True, param=None):
        result = None
        try:
            if param:
                self._cursor.execute(sql, param)
            else:
                self._cursor.execute(sql)
            result = self._cursor.fetchone() if one else self._cursor.fetchall()
        except Exception as error:
            raise error

        return result

    def execute_transact(self, sql, param=None, update=False):
        id = None
        try:
            if param:
                self._cursor.execute(sql, param)
            else:
                self._cursor.execute(sql)
            self._db.commit()
            id = self.cursor.lastrowid if not update else -1
        except Exception as error:
            self._db.rollback()
            # raise error
        return id

    def call_proc_fetch(self, proc_name, args=()):
        sets = []
        try:
            results = self._cursor.callproc(proc_name, args)
            sets.append(self._cursor.fetchall())
            while self._cursor.nextset():
                sets.append(self._cursor.fetchall())

        except Exception as error:
            pass

        return sets

    def close(self):
        try:
            if self._db is not None:
                if self._cursor is not None:
                    self._cursor.close()
                    del self._cursor
                self._db.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

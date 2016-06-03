#!/usr/bin/env python
# coding=utf-8

import config as cfg
from middleware.authentication import Authentication
from middleware.dbconnection import mysql_connection
from werkzeug.security import generate_password_hash, check_password_hash

class Users(object):
    def __init__(self):
        self.connection = mysql_connection()

    def is_user_exist(self, email):
        sql = "SELECT UID FROM {0} WHERE EMAIL = '{1}'".format(cfg.DB["users"], email)
        row = self.connection.execute_fetch(sql)
        return row is not None

    def create_new(self, email, display, password, role, modules=None):
        if self.is_user_exist(email):
            return {"error": "Email already exist in the system"}

        pw_hash = generate_password_hash(password)
        sql = u"INSERT INTO {0} (EMAIL, DISPLAY, PASSWORD, ROLE) VALUES('{1}','{2}','{3}','{4}')".format(cfg.DB["users"], email, display, pw_hash, role)
        uid = self.connection.execute_transact(sql)
        if role == cfg.GLOBAL["user_role"][0] and modules is not None: # 0 user, 1 admin
            for mid in modules:
                sql = u"INSERT INTO {0} (UID,MID) VALUES({1},{2})".format(cfg.DB["module2user"], uid, mid)
                self.connection.execute_transact(sql)
        return uid

    def login(self, email, password):
        if len(email)==0 or len(password) == 0:
            return {"error": "Wrong credentials, please check email/password"}
        sql = "SELECT * FROM {0} WHERE EMAIL = '{1}'".format(cfg.DB["users"], email)
        row = self.connection.execute_fetch(sql)
        if row is None:
            return {"error": "Wrong credentials, please check email/password"}
        pw_hash = row["password"]
        modules = None
        del row["password"]
        result = row
        if check_password_hash(pw_hash, password):
            if row["role"] == cfg.GLOBAL["user_role"][0]: # 0 user, 1 admin
                sql = "SELECT * FROM {0} WHERE UID = {1}".format(cfg.DB["modulesByUser"], row["uid"])
                modules = self.connection.execute_fetch(sql, False)
            result["modules"] = modules
            result["token"] = Authentication.create_token(result)
        else:
             return {"error": "Wrong credentials, please check email/password"}

        return result

    def get_modules(self):
        sql = "SELECT * FROM {0}".format(cfg.DB["modules"])
        return self.connection.execute_fetch(sql, False)

    def get_users(self):
        sql = "SELECT * FROM {0}".format(cfg.DB["allUsers"])
        return self.connection.execute_fetch(sql, False)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

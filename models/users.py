#!/usr/bin/env python
# coding=utf-8

import config as cfg
from middleware.dbconnection import mysql_connection
from werkzeug.security import generate_password_hash, check_password_hash

class Users(object):
    def __init__(self):
        self.connection = mysql_connection()

    def create_new(self, email, display, password, role, modules):
        self.pw_hash = generate_password_hash(password)

    def login(self, email, password):
        return check_password_hash(self.pw_hash, password)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

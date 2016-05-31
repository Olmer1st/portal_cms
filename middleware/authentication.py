#!/usr/bin/env python
# coding=utf-8

import jwt
import config as cfg

class Authentication(object):
    def __init__(self):
        self.token = None
        pass

    def authenticate(self, user_info):
        self.token = jwt.encode(user_info, cfg.GLOBAL["secret_key"], algorithm='HS256')

    def check_token(self, header_token=None):
        print jwt.decode(self.token, cfg.GLOBAL["secret_key"], algorithms=['HS256'])
        return self.token == header_token

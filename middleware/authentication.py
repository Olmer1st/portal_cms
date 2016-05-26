#!/usr/bin/env python
# coding=utf-8


class Authentication(object):
    def __init__(self):
        self.token = None
        pass

    def check_token(self, header_token=None):
        return self.token == header_token

#!/usr/bin/env python
# coding=utf-8

import jwt
import config as cfg


class Authentication:
    @staticmethod
    def create_token(self, user_info):
        return jwt.encode(user_info, cfg.GLOBAL["secret_key"], algorithm='HS256')

    @staticmethod
    def check_token(module_name, request):
        if module_name is None or request is None:
            return False
        header_token=request.headers.get('x-access-token')
        if header_token is None:
            return False
        user_info = jwt.decode(header_token, cfg.GLOBAL["secret_key"], algorithms=['HS256'])
        if user_info is None:
            return False
        if "role" in user_info and user_info["role"] is not None:
            if user_info["role"] =="admin":
                return True

            if "modules" in user_info and len(user_info["modules"])>0:
                result = filter(lambda x: "name" in x and x["name"]==module_name,  user_info["modules"])
                return result is not None and len(result)>0

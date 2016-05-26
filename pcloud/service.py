#!/usr/bin/env python
# coding=utf-8

import json
import requests
import config as cfg


def url_generator(method_name, **kwargs):
    api_url = "{0}/{1}?access_token={2}".format(cfg.PCLOUD["api_url"], method_name, cfg.PCLOUD["access_token"])
    if kwargs:
        for param, value in kwargs.items():
            api_url = api_url + "&" + param + "=" + value

    return api_url


class PCloudService:

    def __init__(self):
        pass

    @staticmethod
    def get_link(folder_name, file_name):
        if not folder_name or not file_name:
            return {"error": "wrong parameters"}
        method = cfg.PCLOUD["methods"]["getfilelink"]
        param = method["params"]["path"]
        param = {"path": param % (folder_name, file_name)}
        url = url_generator(method["name"], **param)
        response = requests.get(url)
        if response.ok:
            return json.loads(response.content)
        return {"error": "no data"}




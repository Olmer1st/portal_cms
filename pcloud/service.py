#!/usr/bin/env python
# coding=utf-8

import json
import requests
import config as cfg
from models.cloud import Cloud


def url_generator(method_name, **kwargs):
    api_url = "{0}/{1}?access_token={2}".format(cfg.PCLOUD["api_url"], method_name, cfg.PCLOUD["access_token"])
    if kwargs:
        for param, value in kwargs.items():
            api_url = api_url + "&" + param + "=" + value

    return api_url


def download_url_generator(method_name, code):
    api_url = "{0}/{1}?code={2}".format(cfg.PCLOUD["api_url"], method_name, code)
    return api_url


class PCloudService:
    def __init__(self):
        pass

    @staticmethod
    def get_link(folder_name, file_name):
        if not folder_name or not file_name:
            return {"error": "wrong parameters"}
        method = cfg.PCLOUD["methods"]["link"]
        param = method["params"]["path"]
        param = {"path": param % (folder_name, file_name)}
        url = url_generator(method["name"], **param)
        response = requests.get(url)
        if response.ok:
            return json.loads(response.content)
        return {"error": "no data"}

    @staticmethod
    def get_download_link(bid, folder_name, file_name):
        if not bid or not folder_name or not file_name:
            return {"error": "wrong parameters"}
        cloud = None
        with Cloud() as cloud_manager:
            cloud = cloud_manager.get_link_by_bid(bid)
            if cloud is None:
                method = cfg.PCLOUD["methods"]["publink"]
                param = method["params"]["path"]
                param = {"path": param % (folder_name, file_name)}
                url = url_generator(method["name"], **param)
                response = requests.get(url)
                if response.ok:
                    cloud = json.loads(response.content)
                    cid = cloud_manager.save_link(bid, cloud["linkid"], cloud["code"])

        method = cfg.PCLOUD["methods"]["download"]
        url = download_url_generator(method["name"], cloud["code"])
        response = requests.get(url)
        if response.ok:
            return json.loads(response.content)
        return {"error": "no data"}

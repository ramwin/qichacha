#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-02-18 15:57:33


import logging
import requests
import time
import hashlib
from . import exceptions


class QichachaClient(object):

    def __init__(self, key, secretkey, logger=None):
        """
        key, secretkey请从 [企查查](http://www.yjapi.com/DataCenter/MyData)获取
        logger是一个logger
        """
        self.key = key
        self.logger = logger
        self.secretkey = secretkey
        if logger is None:
            self.logger = logging.getLogger()

    def get_token(self):
        """
        return: {"timespan": "时间戳字符串", "token: "对应的token"}
        """
        timespan = str(int(time.time()))
        md5 = hashlib.md5()
        md5.update(self.key.encode("UTF-8"))
        md5.update(timespan.encode("UTF-8"))
        md5.update(self.secretkey.encode("UTF-8"))
        token = md5.hexdigest().upper()
        return {"timespan": timespan, "token": token}

    def check(self, response):
        """校验response是否正确"""
        if response.status_code not in [200, 201]:
            self.logger.error(response.status_code)
            raise exceptions.APIException("企查查response不正确")
        data_json = response.json()
        if data_json["Status"] in ["202"]:
            if data_json["Message"] == "传入参数有误，请检查":
                raise exceptions.StupidException()
        if data_json["Status"] not in ["200", "201"]:
            self.logger.error(data_json)
            raise exceptions.APIException("企查查状态码不正确")

    def search(self, name):
        """
        企业关键字模糊查询, 返回
        (公司列表, 具体的response)
        [接口文档地址](http://www.yjapi.com/DataApi/Api?apiCode=410)
        """
        token_dict = self.get_token()
        response = requests.get(
            url="http://api.qichacha.com/ECIV4/Search",
            headers={
                "Token": token_dict["token"],
                "Timespan": token_dict["timespan"],
            },
            params={
                "key": self.key,
                "keyword": name,
                "dtype": "json",
            },
        )
        self.check(response)
        data_json = response.json()
        return data_json["Result"], response

    def get_brief_intro(self, name):
        """
        企业附加信息查询, 返回
        (
            {"KeyNo": "f625a5b661058ba5082ca508f99ffe1b",
             "Name": "苏州朗动网络科技有限公司",
             "Content":, "企查查是一站式企业信息查询平台，通过查询企业信息，
             查看评价，帮助查询人获取相关信息。隶属于苏州朗动网络科技有限公司"
            },
            具体的response
        )
        如果公司不存在， 返回
        (
            None,
            具体的response
        )
        [接口文档地址](http://www.yjapi.com/DataApi/Api?apiCode=215)
        """
        token_dict = self.get_token()
        response = requests.get(
            url="http://api.qichacha.com/ECIAdditional/GetBriefIntroduction",
            headers={
                "Token": token_dict["token"],
                "Timespan": token_dict["timespan"],
            },
            params={
                "key": self.key,
                "companyName": name,
                "dtype": "json",
            },
        )
        self.check(response)
        data_json = response.json()
        return data_json["Result"], response

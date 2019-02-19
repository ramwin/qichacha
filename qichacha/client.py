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
        if response.status_code not in [200, 201]:
            raise exceptions.APIException("搜索公司结果不正确")
        data_json = response.json()
        if data_json["Status"] not in ["200", "201"]:
            self.logger.error(data_json)
            raise exceptions.APIException("搜索公司结果不正确")
        return data_json["Result"], response

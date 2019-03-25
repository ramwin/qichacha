#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-02-18 15:57:33


from __future__ import unicode_literals
import logging
import requests
import time
import hashlib
from . import exceptions

logger = logging.getLogger()


class QichachaClient(object):

    def __init__(self, key, secretkey, logger=logger):
        """
        key, secretkey请从 [企查查](http://www.yjapi.com/DataCenter/MyData)获取
        logger是一个logger
        """
        self.key = key
        self.logger = logger
        self.secretkey = secretkey

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
                self.logger.warning(data_json)
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

    def get_detail(self, name):
        """
        企业关键词精确获取详细信息, 返回
        (
            {
                "Partners": [
                    "StockName": "程维",
                    "StockerType": "自然人股东",
                ],
                "Employees": [
                    {"Name": "程维", "Job": "执行董事",}
                ],
                "ContactInfo": {
                    "WebSite": [
                        {
                            "Name": null,
                            "Url": "www.xiaojukeji.com"
                        }
                    ],
                    "PhoneNumber": "010-62682929",
                    "Email": null
                },
                "Industry": {
                    "IndustryCode": "M",
                    "Industry": "科学研究和技术服务业",
                    "SubIndustryCode": "75",
                    "SubIndustry": "科技推广和应用服务业",
                    "MiddleCategoryCode": "759",
                    "MiddleCategory": "其他科技推广服务业",
                    "SmallCategoryCode": "7590",
                    "SmallCategory": "其他科技推广服务业"
                },
                "KeyNo": "4659626b1e5e43f1bcad8c268753216e",
                "Name": "北京小桔科技有限公司",
                "No": "110108015068911",
                "BelongOrg": "北京市工商行政管理局海淀分局",
                "OperName": "程维",
                "StartDate": "2012-07-10T00:00:00",
                "EndDate": null,
                "Status": "开业",
                "Province": "BJ",
                "UpdatedDate": "2018-06-19T00:15:47",
                "CreditCode": "9111010859963405XW",
                "RegistCapi": "1000万人民币元",
                "EconKind": "有限责任公司(自然人投资或控股)",
                "Address": "北京市海淀区东北旺西路8号院35号楼5层501室",
                "Scope": "技术开发、技术咨询、技术服务、技术推广;基础软件服务;应用",
                "TermStart": "2012-07-10T00:00:00",
                "TeamEnd": "2032-07-09T00:00:00",
                "CheckDate": "2017-12-11T00:00:00",
                "OrgNo": "59963405-X",
                "IsOnStock": "0",
                "StockNumber": null,
                "StockType": null,
                "OriginalName": [],
                "ImageUrl": "https://co-image.qichacha.com/CompanyImage/4659626b1e5e43f1bcad8c268753216e.jpg"
            },
            具体的response
        )
        [接口文档地址](http://www.yjapi.com/DataApi/Api?apicode=410)
        """
        token_dict = self.get_token()
        response = requests.get(
            url="http://api.qichacha.com/ECIV4/GetDetailsByName",
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
        if data_json["Status"] == "201":
            raise exceptions.NotFoundException("企查查没有查到结果")
        return data_json["Result"], response

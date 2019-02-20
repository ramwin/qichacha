#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2019-02-19 09:58:33


class APIException(Exception):
    pass


class NotFoundException(APIException):
    desc = "企查查自己没找到"
    pass


class StupidException(NotFoundException):
    desc = "企查查自己没找到，还说是传入参数有误，请检查。误人子弟"
    pass

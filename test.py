#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-02-18 15:50:07

from qichacha import QichachaClient
from qichacha import exceptions
import unittest


key = input("请输入您的key: ")
secretkey = input("请输入您的secretkey: ")
client = QichachaClient(key=key, secretkey=secretkey, logger=None)


class TestQichachaAPI(unittest.TestCase):

    def test_search(self):
        results = client.search(name="小桔科技")[0]
        self.assertIsInstance(results, list)
        with self.assertRaises(exceptions.StupidException):
            client.search(name="百德珠宝B&D")

    def test_brief_intro(self):
        intro, res = client.get_brief_intro("苏州朗动网络科技有限公司")
        self.assertIsInstance(intro["Content"], str)
        self.assertGreater(len(intro["Content"]), 57)

        intro, res = client.get_brief_intro("不存在的一个公司")
        self.assertIsNone(intro, None)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-02-18 15:50:07


from qichacha import QichachaClient
from qichacha import exceptions
import unittest
import six


if six.PY2:
    input = raw_input
elif six.PY3:
    unicode = str


key = input("请输入您的key: ")
secretkey = input("请输入您的secretkey: ")
client = QichachaClient(key=key, secretkey=secretkey)


class TestQichachaAPI(unittest.TestCase):

    def test_search(self):
        results = client.search(name="小桔科技")[0]
        self.assertIsInstance(results, list)
        with self.assertRaises(exceptions.StupidException):
            client.search(name="百德珠宝B&D")

    def test_brief_intro(self):
        intro, res = client.get_brief_intro("苏州朗动网络科技有限公司")
        if six.PY2:
            self.assertIsInstance(intro["Content"], unicode)
        else:
            self.assertIsInstance(intro["Content"], str)
        self.assertGreater(len(intro["Content"]), 57)

        intro, res = client.get_brief_intro("不存在的一个公司")
        self.assertIsNone(intro, None)

    def test_detail(self):
        detail, res = client.get_detail("北京小桔科技有限公司")
        self.assertIsInstance(detail, dict)
        self.assertEqual(detail["KeyNo"], "4659626b1e5e43f1bcad8c268753216e")
        self.assertEqual(detail["No"], "110108015068911")
        self.assertEqual(detail["OperName"], u"程维")


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-02-18 15:50:07

from qichacha import QichachaClient
import unittest


key = input("请输入您的key: ")
secretkey = input("请输入您的secretkey: ")
client = QichachaClient(key=key, secretkey=secretkey, logger=None)


class TestQichachaAPI(unittest.TestCase):

    def test_search(self):
        results = client.search(name="小桔科技")[0]
        self.assertIsInstance(results, list)


if __name__ == '__main__':
    unittest.main()

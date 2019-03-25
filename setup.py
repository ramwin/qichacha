#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2019-02-18 15:41:36

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qichacha",
    version="0.0.8",
    author="Xiang Wang",
    author_email="ramwin@qq.com",
    description="企查查的api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramwin/qichacha",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

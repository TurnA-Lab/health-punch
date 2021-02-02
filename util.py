#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: util.py
@author: Skye Young
@time: 2021/2/2 0002 16:59
"""

from functools import partial


class F(partial):
    """
    在 Python 中实现管道
    来自：https://www.v2ex.com/t/743574
    """

    def __ror__(self, other):
        if isinstance(other, tuple):
            return self(*other)
        return self(other)

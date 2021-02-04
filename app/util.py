#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: util.py
@author: Skye Young
@time: 2021/2/4 0004 11:52
@description: 
"""
from typing import Union

from passlib.context import CryptContext

"""
加密，用于存入 SQLite 时对密码等进行处理 
来自： https://blog.tecladocode.com/learn-python-encrypting-passwords-python-flask-and-passlib/
"""
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def encrypt(password: Union[str, bytes]) -> Union[str, bytes]:
    return pwd_context.hash(password)


def check_encrypted(password: Union[str, bytes], hashed: Union[str, bytes]) -> bool:
    return pwd_context.verify(password, hashed)

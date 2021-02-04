#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: config.py
@author: Skye Young
@time: 2021/2/3 0003 23:41
@description: 环境配置
"""
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = '自动健康打卡'
    version: str = '0.1.0'

    # 需要传入的
    DB_PATH: str
    SECRET_KEY: str
    ROOT_ACCOUNT: str
    ROOT_PASSWD: str

    class Config:
        # 可以使用 .env
        env_file = '.env'
        env_file_encoding = 'utf-8'
        # 也可以使用 Docker Secrets
        # docker secrets default location
        # secrets_dir = '/run/secrets'


@lru_cache()
def get_settings():
    """
    获取配置
    :return:
    """
    return Settings()

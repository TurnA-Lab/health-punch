#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: database.py
@author: Skye Young
@time: 2021/2/4 0004 0:47
@description: 
"""
# import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

db_path = get_settings().db_path

SQLALCHEMY_DATABASE_URL = f'sqlite:///{db_path}'

# if (not os.path.exists(os.path.dirname(db_path))) or (not os.path.exists(db_path)):
#     os.mkdir(os.path.dirname(db_path))

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

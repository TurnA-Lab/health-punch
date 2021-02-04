#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: database.py
@author: Skye Young
@time: 2021/2/4 0004 0:47
@description: 
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

SQLALCHEMY_DATABASE_URL = f'sqlite:///{get_settings().DB_PATH}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

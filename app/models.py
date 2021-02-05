#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: models.py
@author: Skye Young
@time: 2021/2/4 0004 0:53
@description: 
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database import Base


class User(Base):
    __tablename__ = 'basic_user'

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String, unique=True, index=True)
    password = Column(String)
    deleted = Column(Boolean, default=False)

    # user_action_log = relationship('User', back_populates='user')


class UserActionLog(Base):
    __tablename__ = 'user_action_log'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('basic_user.id'))
    time = Column(String)
    success = Column(Boolean)
    description = Column(String, nullable=True)

    # user = relationship('User', back_populates='user_action_log')

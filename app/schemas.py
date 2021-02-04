#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: schemas.py
@author: Skye Young
@time: 2021/2/4 0004 11:25
@description: 
"""
from typing import Optional

from pydantic.main import BaseModel


class UserActionLogBase(BaseModel):
    time: str
    success: bool
    description: Optional[str] = None


class UserActionLogCreate(UserActionLogBase):
    pass


class UserActionLog(UserActionLogBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    account: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    deleted: bool

    class Config:
        orm_mode = True

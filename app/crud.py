#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: crud.py
@author: Skye Young
@time: 2021/2/4 0004 11:51
@description: 
"""
from passlib.handlers.cisco import cisco_type7
from sqlalchemy.orm import Session

from app.models import User, UserActionLog
from app.schemas import UserCreate, UserActionLogCreate
from app.util import check_encrypted


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_account(db: Session, account: str):
    return db.query(User).filter(User.account == account).first()


def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    new_user = User(account=user.account, password=cisco_type7.hash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id)
    user.update({'deleted': True})
    db.commit()
    return user


def delete_user_by_account(db: Session, account: str):
    user = db.query(User).filter(User.account == account)
    user.update({'deleted': True})
    db.commit()
    return user


def verify_user_password(db: Session, account: str, password: str):
    user = db.query(User).filter(User.account == account).first()
    return check_encrypted(password, user.encrypted)


def update_user_password(db: Session, account: str, password: str):
    user = db.query(User).filter(User.account == account)
    user.update({'password': cisco_type7.hash(password)})
    db.commit()
    return user


def get_user_action_logs(db: Session, user_id: int, skip: int = 0, limit: int = 50):
    return db.query(UserActionLog).filter(UserActionLog.user_id == user_id).offset(skip).limit(limit).all()


def get_user_action_logs_by_account(db: Session, account: str, skip: int = 0, limit: int = 50):
    user_id = get_user_by_account(db, account)
    return get_user_action_logs(db, user_id, skip, limit)


def get_user_action_logs_all(db: Session, skip: int = 0, limit: int = 50):
    return db.query(UserActionLog).offset(skip).limit(limit).all()


def create_user_action_log(db: Session, action_log: UserActionLogCreate, user_id: int):
    new_item = UserActionLog(**action_log.dict(), user_id=user_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item

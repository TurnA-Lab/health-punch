#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: web.py
@author: Skye Young
@time: 2021/2/5 0005 1:39
@description: 
"""

from typing import Union

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from config import Settings, get_settings
from database import Base, engine, SessionLocal
from schemas import User, UserCreate, UserActionLog
from util import Logger

Base.metadata.create_all(bind=engine)

app = FastAPI()


# TODO: 单独的管理账户
# TODO: 权限


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/info')
async def info(settings: Settings = Depends(get_settings)):
    return {
        'app_name': settings.app_name,
        'version': settings.version
    }


@app.get('/user/', response_model=User)
def get_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    return users


@app.get('/user/{id_account}', response_model=User)
def get_user(id_account: Union[int, str], db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id_account) if len(id_account) > 4 \
        else crud.get_user_by_account(db, str(id_account))
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.post('/user/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_account(db, user.account)
    if db_user is not None:
        raise HTTPException(status_code=404, detail='Account already exists')
    return crud.create_user(db, user)


@app.delete('/user/{id_account}', response_model=User)
def delete_user(id_account: Union[int, str], db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, id_account) if len(id_account) > 4 \
        else crud.get_user_by_account(db, str(id_account))
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.get('/log/', response_model=UserActionLog)
def get_logs_all(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    logs = crud.get_user_action_logs(db, skip, limit)
    return logs


@app.get('/log/{id_account}', response_model=UserActionLog)
def get_logs(id_account: Union[int, str], skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    logs = crud.get_user_action_logs(db, id_account, skip, limit) if type(id_account) is int \
        else crud.get_user_action_logs_by_account(db, id_account, skip, limit)
    if logs is None:
        raise HTTPException(status_code=404, detail='Log not found')
    return logs


def main():
    Logger(__name__).get_log().info('Start Init Server')
    uvicorn.run(app, host='0.0.0.0', port=get_settings().PORT)
    pass


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: web.py
@author: Skye Young
@time: 2021/2/5 0005 1:39
@description: 
"""
from typing import List

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.config import Settings, get_settings
from app.database import Base, engine, SessionLocal
from app.scheduler import health_punch_task
from app.schemas import User, UserCreate, UserActionLog
from app.util import Logger

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


@app.get('/users/', response_model=List[User])
def get_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, limit)
    if users is None:
        raise HTTPException(status_code=404, detail='Users not found')
    return users


@app.get('/users/{id_account}', response_model=User)
def get_user(id_account: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, int(id_account)) if len(id_account) < 4 \
        else crud.get_user_by_account(db, id_account)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.post('/users/', response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_account(db, user.account)

    if db_user is not None:
        raise HTTPException(status_code=404, detail='Account already exists')
    return crud.create_user(db, user)


@app.delete('/users/{id_account}', response_model=User)
def delete_user(id_account: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, int(id_account)) if len(id_account) < 4 \
        else crud.delete_user_by_account(db, id_account)

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.get('/logs/', response_model=List[UserActionLog])
def get_logs_all(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    logs = crud.get_user_action_logs_all(db, skip, limit)
    if logs is None:
        raise HTTPException(status_code=404, detail='Logs not found')
    return logs


@app.get('/logs/{id_account}', response_model=List[UserActionLog])
def get_logs(id_account: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    logs = crud.get_user_action_logs(db, int(id_account), skip, limit) if len(id_account) < 4 \
        else crud.get_user_action_logs_by_account(db, id_account, skip, limit)
    if logs is None:
        raise HTTPException(status_code=404, detail='Log not found')
    return logs


@app.get('/punch/', response_model=List[UserActionLog])
def exec_task(db: Session = Depends(get_db)):
    logs = crud.get_user_action_logs_all(db)
    health_punch_task(db)
    new_logs = crud.get_user_action_logs_all(db)
    diff_logs = list(set(new_logs).difference(set(logs)))
    if diff_logs is None:
        raise HTTPException(status_code=404, detail='Log not found')
    return diff_logs


def main():
    Logger(__name__).get_log().info('Start Init Server')
    uvicorn.run(app, host='0.0.0.0', port=get_settings().PORT)
    pass


if __name__ == '__main__':
    main()

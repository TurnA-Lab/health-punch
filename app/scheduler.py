#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: scheduler.py
@author: Skye Young
@time: 2021/2/4 0004 22:50
@description: 
"""
from datetime import datetime
from typing import List

from apscheduler.schedulers.blocking import BlockingScheduler
from passlib.handlers.cisco import cisco_type7
from sqlalchemy.orm import Session

from app.config import get_settings
from app.crud import get_user_by_account, create_user_action_log
from app.models import User
from app.schemas import UserActionLogCreate
from app.web import get_db
from health_punch import inited_session, F, login, lets_punch, logout, StepErr


def health_punch():
    db: Session = next(get_db())
    users: List[User] = db.query(User).all()
    sess = inited_session()

    for user in users:
        user_id = get_user_by_account(db, user.account).id
        success = True
        description = ''

        try:
            assert sess \
                   | F(login, username=user.account, password=cisco_type7.decode(user.password)) \
                   | F(lets_punch, username=user.account) \
                   | F(logout) is None
        except StepErr as err:
            success = False
            description = str(err)

        action_log = UserActionLogCreate(time=str(datetime.now()), success=success, description=description)
        create_user_action_log(db, action_log, user_id)


def main():
    scheduler = BlockingScheduler({
        'apscheduler.jobstores.default': {
            'type': 'sqlalchemy',
            'url': f'sqlite:///{get_settings().DB_PATH}'
        },
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.job_defaults.max_instances': '3',
        'apscheduler.timezone': 'Asia/Shanghai',
    })

    scheduler.add_job(health_punch, 'cron', hour=8)

    try:
        scheduler.start()
    except SystemExit:
        print('Scheduler Stopped')
    pass


if __name__ == '__main__':
    main()

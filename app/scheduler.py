# !/usr/bin/env python3
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
from app.util import Logger
from app.web import get_db

log = Logger(__name__).get_log()


# TODO: 执行失败后，放入另一个队列，再执行一次
# TODO: 执行失败两次后，发起通知
# TODO: 通知接入 Server 酱，或邮件
def health_punch_task():
    from health_punch import inited_session, F, login, lets_punch, logout, StepErr

    db: Session = next(get_db())
    users: List[User] = db.query(User).all()
    sess = inited_session()

    for user in users:
        user_id = get_user_by_account(db, user.account).id
        success = True
        description = ''

        log.info(f'Start Health Punch Task For ID-{user_id}')
        try:
            assert sess \
                   | F(login, username=user.account, password=cisco_type7.decode(user.password)) \
                   | F(lets_punch, username=user.account) \
                   | F(logout) is None
            log.info(f'Task For ID-{user_id} Succeed')
        except StepErr as err:
            success = False
            description = str(err)
            log.warn(f'Task For ID-{user_id} Failed')

        action_log = UserActionLogCreate(time=str(datetime.now()), success=success, description=description)
        create_user_action_log(db, action_log, user_id)


def main():
    settings = get_settings()

    log.info('Start Init Scheduler')

    scheduler = BlockingScheduler({
        'apscheduler.jobstores.default': {
            'type': 'sqlalchemy',
            'url': f'sqlite:///{settings.db_path}'
        },
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.job_defaults.max_instances': '3',
        'apscheduler.timezone': 'Asia/Shanghai',
    })

    scheduler.add_job(health_punch_task, 'cron', hour=settings.TASK_HOUR, minute=settings.TASK_MINUTE)
    log.info('Scheduler Added Health Punch Task')

    try:
        log.info('Scheduler Inited')
        scheduler.start()
    except SystemExit:
        log.info('Scheduler Stopped')
    pass


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: main.py
@author: Skye Young
@time: 2021/2/5 0005 14:38
@description: 
"""
from multiprocessing.context import Process

from app.scheduler import main as scheduler_main
from app.util import Logger
from app.web import main as web_main


def main():
    web_process = Process(target=web_main)
    scheduler_process = Process(target=scheduler_main)

    web_process.daemon = True
    scheduler_process.daemon = True

    web_process.start()
    scheduler_process.start()

    web_process.join()
    scheduler_process.join()

    Logger(__name__).get_log().info('All Stopped')
    pass


if __name__ == '__main__':
    main()

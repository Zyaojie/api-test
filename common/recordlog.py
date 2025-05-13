# -*- coding: utf-8 -*-
'''
@Author      : Zyaojie
@File        : recordlog.py
@Created     : 2025/5/12 11:13
@Description : 
'''
import logging
import os
import time

from conf import setting


log_path = setting.FILE_PATH['Log']

if not os.path.exists(log_path): os.mkdir(log_path)

logfile_name = log_path + 'test.{}.log'.format(time.strftime("%Y-%m-%d"))
print(logfile_name)
class RecordLog:
    '''封装日志'''
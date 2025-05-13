# -*- coding: utf-8 -*-
'''
@Author      : Zyaojie
@File        : conftest.py.py
@Created     : 2025/5/9 10:16
@Description : 
'''
import pytest
from common.recordlog import logs
'''
-function: 每一个函数和方法都会执行一次
-class: 每一个类调用一次，一个类中可以有多个方法
-module：每一个.py文件调用一次，该文件中可以有多个类
-session：是多个文件调用一次，可以跨.py文件调用，每个.py就是module，整个就执行一次
-autouse: 默认为False，不会自动执行，需要手动调用，为true可自动执行
-yield: 前置、后置处理if node_name in extract_data:
    print(extract_data[node_name])
else:
    print(f"{node_name} not found in extract_data")
'''

@pytest.fixture(scope='session',autouse=True)
# scope:作用域，params:参数化，autouse:自动使用，ids:自定义ID，name:名称
def fixture_test(request):
    '''前后置处理'''
    logs.info('--------------------接口测试开始--------------------')
    yield
    logs.info('--------------------接口测试结束--------------------')

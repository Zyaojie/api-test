# -*- coding: utf-8 -*-
# @Time : 2025/5/5 16:05
# @Author : Zyaojie
# @File : test_login
# @Project : apitest
import pytest

class TestLogin:
    def setup_class(self):
        '''在所有测试用例执行前只执行一次'''


    def setup(self):
        '''前置处理'''
        print('在每个测试方法运行前都要执行我的代码')

    def test_case01(self):
        print('我第二个执行')

    #@pytest.mark.skip #跳过
    def test_case02(self):
        print('我第三个执行')

    def test_case03(self):
        print('我第一个执行')

    def teardown(self):
        '''后置处理'''
        print('在每个测试方法运行后都要执行我的代码')
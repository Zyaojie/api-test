# -*- coding: utf-8 -*-
# @Time : 2025/5/5 16:05
# @Author : Zyaojie
# @File : test_login
# @Project : apitest
import pytest
from common.readyaml import get_testcase_yaml



class TestLogin:

    def test_case01(self):
        print('用例1')

    #@pytest.mark.skip #跳过
    def test_case02(self):
        print('用例2')

    def test_case03(self,fixture_test):
        print('用例3')

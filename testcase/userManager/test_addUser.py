# -*- coding: utf-8 -*-
# @Time : 2025/5/5 16:10
# @Author : Zyaojie
# @File : test_addUser
# @Project : apitest
import pytest

class TestAddUser:

    @pytest.mark.usermanager
    def test_case01(self):

        print('新增用户')

    @pytest.mark.smock
    def test_case02(self):
        print('删除用户')

    def test_case03(self):
        print('修改用户')

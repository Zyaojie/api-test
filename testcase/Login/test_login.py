# -*- coding: utf-8 -*-
# @Time : 2025/5/5 16:05
# @Author : Zyaojie
# @File : test_login
# @Project : apitest
import pytest
from common.readyaml import get_testcase_yaml
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequests

class TestLogin:
    @pytest.mark.parametrize('params', get_testcase_yaml(
        './testcase/Login/login.yaml'))  # 支持的数据类为列表、元祖、字典列表、字典元祖、参数里面有多少个值，这个用例就会执行多少次
    def test_case01(self, params):
        url = params['baseInfo']['url']
        new_url = 'http://127.0.0.1:8787' + url
        method = params['baseInfo']['method']
        headers = params['baseInfo']['header']
        data = params['testCase'][0]['data']
        send = SendRequests()
        res = send.run_main(url=new_url,data=data,header=None,method=method)
        print(res)
        assert res['msg'] == '登录成功'

    @pytest.mark.parametrize('params', get_testcase_yaml(
        './testcase/Login/login.yaml'))  # 支持的数据类为列表、元祖、字典列表、字典元祖、参数里面有多少个值，这个用例就会执行多少次
    def test_case02(self, params):
        url = params['baseInfo']['url']
        new_url = 'http://127.0.0.1:8787' + url
        method = params['baseInfo']['method']
        headers = params['baseInfo']['header']
        data = {'user_name':'test02','passwd':'123'}
        send = SendRequests()
        res = send.run_main(url=new_url, data=data, header=None, method=method)
        print(res)
        assert res['msg'] == '登录成功'
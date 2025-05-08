# -*- coding: utf-8 -*-
# @Time : 2025/5/5 16:05
# @Author : Zyaojie
# @File : test_login
# @Project : apitest
import pytest
from common.readyaml import get_testcase_yaml


@pytest.fixture(scope='function',autouse=True,params=['1','2','3'])
# scope:作用域，params:参数化，autouse:自动使用，ids:自定义ID，name:名称
def fixture_test(request):
    '''前后置处理'''
    #print('--------------------接口测试开始--------------------')
    #yield
    #print('--------------------接口测试结束--------------------')
    return request.param
class TestLogin:

    def test_case01(self):
        print('用例1')

    #@pytest.mark.skip #跳过
    def test_case02(self):
        print('用例2')
    @pytest.mark.maoyan
    def test_case03(self,fixture_test):
        print('用例3')
        print('获取到的参数值为：',fixture_test)

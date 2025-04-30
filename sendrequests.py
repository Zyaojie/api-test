# -*- coding: utf-8 -*-
'''
@Author      : Zyaojie
@File        : sendrequests.py
@Created     : 2025/4/16 15:08
@Description : 
'''
import requests
import json


class SendRequests(object):
    """
    封装接口请求
    """

    def __init__(self):
        pass

        def get(self, url, data, header):
            '''
            封装get请求
        :param url: 请求地址
        :param data: 请求参数
        :param header: 请求头
        :return:

            '''

            if header is None:
                res = requests.get(url=url, params=data)
                #get请求允许关键字传参，因为GET请求的参数必须附加在 URL 末尾
            else:
                res = requests.get(url=url, params=data, headers=header)
            return res.json()

    def post(self, url, data, header):
        """
        封装post请求()
        :param url: 请求地址
        :param data: 请求参数
        :param header: 请求头
        :return:
        """
        if header is None:
            res = requests.post(url, data, verify=False)
            #post请求使用形参传参，因为POST 请求的参数可以放在 请求体（Body） 中，且支持多种格式（如表单、JSON、二进制等）
        else:
            res = requests.post(url, data, headers=header, verify=False)
        return res.json()

    def put(self):
        pass

    def delete(self):
        pass

    def run_main(self, url, data, header, method):
        '''
        接口请求主函数
        :param url: 请求地址
        :param data: 请求参数
        :param header: 请求头
        :param method: 请求方法
        :return:
        '''
        if method.upper() == 'GET':
            res = self.get(url, data, header)
            #相当于直接调用该类中的get请求 好处是一处定义多处使用，修改是只需要修改该类中的get方法
            #（调用当前类里的方法写法self.类名，两种情况不需要一个是静态方法，一个是类方法）
        elif method.upper() == 'POST':
            res = self.post(url, data, header)
        else:
            print('暂时只支持get和post请求')
        return res


if __name__ == '__main__':
    url = 'http://127.0.0.1:8787/dar/user/login'
    data = {
        "user_name": "test01",
        "passwd": "admin123"
    }
    method = 'post'
    header = None
    send = SendRequests()
    res = send.run_main(url=url, data=data, header=header, method=method)
    print(res)

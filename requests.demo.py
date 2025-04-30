# -*- coding: utf-8 -*-
# @Time : 2025/4/7 20:59
# @Author : 17507
# @File : requests.demo.py
# @Project : apitest
import requests
from requests import utils

url = 'http://127.0.0.1:8787/dar/user/login'

header = {'Content-Type' : 'application/x-www-formurlencoded;charset=UTF-8'}

data = {
    'user_name' : 'test01',
    'passwd' : 'admin123'
}

res = requests.post(url=url,data=data)

#获取cookie

session = requests.session()
#访问接口请求
result = session.request(method='post',url=url,data=data)#访问接口请求

#使用requests中的utils方法来获取cookie
cookie = requests.utils.dict_from_cookiejar(result.cookies)

print(cookie)
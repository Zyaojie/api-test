# -*- coding: utf-8 -*-
# @Time : 2025/4/17 20:01
# @Author : Zyaojie
# @File : readyaml
# @Project : apitest
import os.path

import yaml


# get_testcase_yaml方法解析需传入一个文件路径 根据所传的文件路径打开并读取该文件数据
def get_testcase_yaml(file):
    '''

    :param file: yaml文件的路径
    :return:
    '''
    try:
        with open(file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)  # 读取f文件的yaml数据
            return yaml_data
    except Exception as e:
        print(e)


class ReadyamlData:
    """读取yaml数据，以及写入数据到yanl文件"""

    def __init__(self,yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file

        else:
            self.yaml_file = 'login.yaml'

    def with_yaml_data(self,value):
        """
        写入数据到yaml文件
        :param value:(dict)写入的数据
        :return:
        """
        file_path = 'extract.yaml'
        if not os.path.exists(file_path):
            # 创建空文件
            with open(file_path, 'w', encoding='utf-8') as f:
                #不对文件进行任何操作
                pass

        file = open(file_path,'a',encoding='utf-8')
        if isinstance(value,dict):
            # allow_unicode=True的意思为允许中文字符，sort_keys=False的意思为不对字典进行排序
            write_data = yaml.dump(value,allow_unicode=True,sort_keys=False)
            # 将数据写入yaml文件
            file.write(write_data)



if __name__ == '__main__':
    res = get_testcase_yaml('Login.yaml')[0]
    print(res)
    url = res['baseInfo']['url']
    new_url = 'http://127.0.0.1:8787' + url
    print(new_url)
    method = res['baseInfo']['method']
    data = res['testCase'][0]['data']
    from sendrequests import SendRequests
    send = SendRequests()
    res = send.run_main(method = method,url=new_url,data=data,header=None)
    print(res)
    token = res.get('token')

    write_data = {}
    write_data['token'] = token
    read = ReadyamlData()
    read.with_yaml_data(write_data)
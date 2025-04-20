# -*- coding: utf-8 -*-
# @Time : 2025/4/17 20:01
# @Author : Zyaojie
# @File : readyaml
# @Project : apitest
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

# -*- coding: utf-8 -*-
# @Time : 2025/4/17 20:01
# @Author : Zyaojie
# @File : readyaml
# @Project : apitest
import os.path

import yaml
from conf.setting import FILE_PATH
from common.sendrequests import SendRequests

# get_testcase_yaml方法解析需传入一个文件路径 根据所传的文件路径打开并读取该文件数据
# 定义读取YAML测试用例文件的函数
def get_testcase_yaml(file):
    '''
    安全读取YAML格式的测试用例文件
    :param file: yaml文件的路径
    :return: 解析后的Python数据结构（通常是字典或列表）
    '''
    try:
        # 使用with语句确保文件正确关闭，utf-8编码防止中文乱码
        with open(file, 'r', encoding='utf-8') as f:
            # 使用safe_load避免执行任意代码的风险，比load()更安全
            yaml_data = yaml.safe_load(f)  # 将YAML内容转换为Python数据结构
            return yaml_data
    except Exception as e:
        # 捕获所有异常并打印，但未处理异常可能导致调用方收到None
        print(e)
        # 注意：生产环境应考虑将异常抛给调用方处理


class ReadyamlData:
    """YAML文件读写操作类，封装常用操作"""

    def __init__(self, yaml_file=None):
        # 初始化支持自定义yaml文件路径
        # 设计考虑：提供默认文件名降低调用复杂度
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            # 默认使用login.yaml，适合登录相关配置场景
            self.yaml_file = '../testcase/Login/Login.yaml'

    def with_yaml_data(self, value):
        """
        追加数据到YAML文件（支持中文）
        :param value: 要写入的字典数据
        :return: None
        设计要点：
        1. 自动处理文件不存在的情况
        2. 支持中文编码
        3. 保持字典原始顺序
        """
        file = None
        file_path = FILE_PATH['extract']  # 固定输出文件名，与初始化参数解耦

        # 防御性编程：确保文件存在
        if not os.path.exists(file_path):
            # 创建空文件作为初始化
            # 使用with保证文件正确关闭，pass表示不写入内容
            with open(file_path, 'w', encoding='utf-8') as f:
                pass  # 空文件是合法的YAML(null)

        try:
            # 注意：这里未使用with语句，需要手动关闭文件
            file = open(file_path, 'a', encoding='utf-8')
            # 类型检查确保数据有效性
            if isinstance(value, dict):
                # dump配置说明：
                # allow_unicode=True - 允许中文正常存储
                # sort_keys=False - 保持字典键的原始顺序
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)

                # 实际写入操作
                file.write(write_data)
            else:
                print('写入到【extract.yaml】文件的数据必须为字典类型')
        except Exception as e:
            print(e)
        #手动关闭文件
        finally:
            file.close()

    # def get_extract_yaml(self,node_name):
    #     '''
    #     读取接口提取的变量值
    #     :param node_name:yaml文件的key值
    #     :return:
    #     '''
    #     if os.path.exists('../extract.yaml'):
    #         pass
    #     else:
    #         print('extract.yaml不存在')
    #         file = open('../extract.yaml', 'w')
    #         file.close()
    #         print('extract.yaml创建成功！')
    #
    #
    #     with open('../extract.yaml', 'r', encoding='utf-8') as rf:
    #         extract_data = yaml.safe_load(rf)
    #         return extract_data[node_name]


    def get_extract_data(self,node_name,sec_node_name = None):
        '''
        获取指定extract.yaml
        :param node_name:yaml里面的key值
        :param sec_node_name:
        :return:
        '''
        file_path = FILE_PATH['extract']

        if os.path.exists(file_path):
            pass
        else:
            print('extract.yaml不存在')
        try:
            with open(file_path,'r',encoding='UTF-8') as f:
                ext_data = yaml.safe_load(f)
                if sec_node_name is None:
                    return ext_data[node_name]
                else:
                    return ext_data[node_name][sec_node_name]
        except Exception as e:
            print(e)





if __name__ == '__main__':
    res = get_testcase_yaml('../testcase/Login/Login.yaml')[0]
    url = res['baseInfo']['url']
    new_url = 'http://127.0.0.1:8787' + url
    method = res['baseInfo']['method']
    data = res['testCase'][0]['data']
    from common.sendrequests import SendRequests

    send = SendRequests()
    # res = send.run_main(method=method, url=new_url, data=data, header=None)

    read = ReadyamlData()
    # re = read.get_extract_yaml('Token')
    # print(re)
    extract_data = read.get_extract_data('cookie','session')
    print(extract_data)
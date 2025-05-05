# -*- coding: utf-8 -*-
# @Time : 2025/5/3 17:30
# @Author : Zyaojie
# @File : apiuti
# @Project : apitest
import json
from common.debugtalk import DeugTalk
from common.readyaml import ReadyamlData,get_testcase_yaml



class BaseRequests:
    def __init__(self):
        self.read = ReadyamlData()

    def replace_load(self,data):
        """yaml文件替换解析有${}格式的数据"""
        str_data = data
        if not isinstance(data,str):
            str_data = json.dumps(data,ensure_ascii=False)
        for i in range(str_data.count('${')):

            if "${" in str_data and "}" in str_data:
                #index检测字符串是否子字符串，并找到字符串的索引位置
                start_index = str_data.index("$")
                end_index = str_data.index("}",start_index)

                ref_all_params = str_data[start_index:end_index+1]
                # print(ref_all_params)
                # 取出函数名
                func_name = ref_all_params[2:ref_all_params.index('(')]
                # print(func_name)
                # 取出函数里面的参数值
                funcs_params = ref_all_params[ref_all_params.index('(')+1:ref_all_params.index(')')]
                # print(funcs_params)
                #传入替换的参数获取对应的值
                # print('yaml文件解析前：',str_data)
                extract_data = getattr(DeugTalk(),func_name)(*funcs_params.split(',') if funcs_params else '')
                str_data=str_data.replace(ref_all_params,str(extract_data))
                # print('yaml文件解析后：',str_data)

        # 还原数据
        if data and isinstance(data,dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data



if __name__ == '__main__':
    data = get_testcase_yaml('../testcase/Login/Login.yaml')[0]
    base = BaseRequests()
    res = base.replace_load(data)
    print(res)
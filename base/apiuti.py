# -*- coding: utf-8 -*-
# @Time : 2025/5/3 17:30
# @Author : Zyaojie
# @File : apiuti
# @Project : apitest
import json
from common.debugtalk import DeugTalk
from common.readyaml import ReadyamlData,get_testcase_yaml
from conf.operationConfig import OperationConfig
import allure

class BaseRequests:
    def __init__(self):
        self.read = ReadyamlData()
        self.conf = OperationConfig()

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

    def specifcation_yaml(self, case_info):
        """
        规范yaml接口测试数据的写法
        :param case_info: list类型，调试取case_info[0]
        :return:
        """

        params_type = ['params','data','json']
        cookie = None  # 初始化 cookie 变量

        try:
            base_url = self.conf.get_envi('host')
            url = base_url + case_info['baseInfo']['url']
            allure.attach(url, f'接口地址：{url}')
            api_name = case_info['baseInfo']['api_name']
            allure.attach(api_name, f'接口名称：{api_name}')
            method = case_info['baseInfo']['method']
            allure.attach(method, f'请求方法：{method}')
            header = case_info['baseInfo']['header']
            allure.attach(str(header), f'请求头：{header}', allure.attachment_type.TEXT)

            try:
                cookie = self.replace_load(case_info['baseInfo']['cookies'])
                allure.attach(cookie, f'cookie：{cookie}', allure.attachment_type.TEXT)
            except:
                pass

            for tc in case_info['testCase']:
                case_name = tc.pop('case_name')
                allure.attach(case_name, f'测试用例名称：{case_name}')
                validation = tc.pop('validation')
                extract = tc.pop('extract', None)
                extract_list = tc.pop('extract_list', None)

                # 替换每个测试用例中的 params, data, json 字段
                for key, value in tc.items():
                    if key in params_type:
                        tc[key] = self.replace_load(value)

                res = self.send.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                         cookies=cookie, file=None, **tc)
                res_text = res.text
                allure.attach(res.text, f'接口的响应信息:{res.text}', allure.attachment_type.TEXT)
                allure.attach(str(res.status_code), f'接口的状态码：{res.status_code}', allure.attachment_type.TEXT)

                res_json = res.json()
                if extract is not None:
                    self.extract_data(extract, res_text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res_text)

                # 处理接口断言
                assert_res.assert_result(validation, res_json, res.status_code)

        except Exception as e:
            logs.error(e)
            raise e


if __name__ == '__main__':
    data = get_testcase_yaml('../testcase/Login/Login.yaml')[0]
    base = BaseRequests()
    res = base.replace_load(data)
    print(res)
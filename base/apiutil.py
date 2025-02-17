import json
from common.readyaml import ReadyamlData, get_testcase_yaml
from common.debugtalk import Debugtaik
from conf.operationConfig import OperationConfig
import allure
from common.sendrequests import SendRequest
from common.recordlog import logs
from conf.setting import FILE_PATA
from common.recordlog import logs
import allure
import re
import jsonpath
from common.assertions import Assertions

assert_res = Assertions()


class RequestsBase(object):

    def __init__(self):
        self.read = ReadyamlData()
        self.conf = OperationConfig()
        self.send = SendRequest()

    def replace_load(self, data):
        '''递归替换 YAML 文件中的 ${} 格式占位符'''

        # **递归处理字典**
        if isinstance(data, dict):
            return {key: self.replace_load(value) for key, value in data.items()}

        # **递归处理列表**
        elif isinstance(data, list):
            return [self.replace_load(item) for item in data]

        # **处理字符串中的占位符**
        elif isinstance(data, str):
            while '${' in data and '}' in data:
                start_index = data.index('${')
                end_index = data.index('}', start_index)

                ref_all_params = data[start_index:end_index + 1]  # 获取完整的占位符
                func_name = ref_all_params[2:ref_all_params.index('(')]  # 获取方法名
                funcs_params = ref_all_params[ref_all_params.index('(') + 1:ref_all_params.index(')')]  # 获取参数

                try:
                    # 调用 Debugtaik 的方法，传入参数
                    if funcs_params:
                        param_list = funcs_params.split(',')
                        extract_data = getattr(Debugtaik(), func_name)(*param_list)
                    else:
                        extract_data = getattr(Debugtaik(), func_name)()

                    # 替换占位符
                    data = data.replace(ref_all_params, str(extract_data))

                except Exception as e:
                    print(f"调用 {func_name} 失败: {e}")
        return data

    def specifcation_yaml(self, case_info):
        """
        规范yaml接口测试数据的写法
        :param case_info: list类型，调试取case_info[0]
        :return:
        """

        cookie = None  # 初始化 cookie 变量

        try:
            params_type = ['params', 'data', 'json']
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

    def extract_data(self, testcase_extract, response):
        """
        提取接口返回值，支持正则表达式提取以及json提取器
        :param testcase_extract:
        :param response:接口的实际返回值
        :return:
        """
        try:
            pattenr_lst = ['(.+?)', '(.*?)', r'(\d+)', r'(\d*)']
            for key, value in testcase_extract.items():
                # 处理正则表达式的提取
                for pat in pattenr_lst:
                    if pat in value:
                        ext_list = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_list.group(1))}
                        else:
                            extract_data = {key: ext_list.group(1)}
                        logs.info(f'正则表达式提取到的参数：{extract_data}')
                        self.read.write_yaml_data(extract_data)
                # 处理json提取器
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    if ext_json:
                        extract_data = {key: ext_json}
                    else:
                        extract_data = {key: '未提取到数据，该接口返回值为空或者json提取表达式有误！'}
                    logs.info(f'json提取器提取到的参数：{extract_data}')
                    self.read.write_yaml_data(extract_data)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件的extract表达式是否正确！')

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml_data(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml_data(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    req = RequestsBase()
    data = get_testcase_yaml('../testcase/Login/login.yaml')[0]
    # req.replace_load(data)
    print(req.specifcation_yaml(data))

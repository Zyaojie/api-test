# -*- coding: utf-8 -*-
# @Time : 2025/5/4 22:04
# @Author : Zyaojie
# @File : operationConfig
# @Project : apitest
import configparser
from conf.setting import FILE_PATH


class OperationConfig:
    '''封装读取ini配置文件的类，提供便捷的配置访问方法'''

    def __init__(self, file_path=None):
        '''
        初始化方法，用于创建配置解析器并加载配置文件
        :param file_path: 可选参数，指定配置文件的路径。如果不提供，则使用默认路径
        '''

        # 检查是否传入了文件路径
        if file_path is None:
            # 如果没有传入路径，使用预设的默认路径（FILE_PATH需要在外部定义）
            # 这里使用双下划线前缀表示私有变量，防止外部直接修改
            self.__file_path = FILE_PATH['conf']
        else:
            # 如果传入了路径，使用传入的路径
            self.__file_path = file_path

        # 创建ConfigParser对象，用于解析INI文件
        self.conf = configparser.ConfigParser()

        try:
            # 尝试读取配置文件，指定UTF-8编码以防止中文乱码
            # read()方法可以接受文件路径列表，这里只传单个文件
            self.conf.read(self.__file_path, encoding='UTF-8')
        except Exception as e:
            # 如果读取失败，打印错误信息（实际项目中建议使用日志记录）
            print(e)

    def get_section_for_data(self, section, option):
        '''
        获取配置文件中指定section下的option值
        :param section: 配置文件中的节名称（如[database]）
        :param option: 节中的选项名称（如host,port）
        :return: 返回配置值，如果出错返回None
        '''
        try:
            # 使用ConfigParser的get方法获取指定section和option的值
            data = self.conf.get(section, option)
            return data
        except Exception as e:
            # 如果获取失败（如section或option不存在），打印错误
            print(e)
            # 这里没有return，默认会返回None

    def get_envi(self, option):
        '''
        专门获取[api_envi]节下的配置值
        :param option: 选项名称
        :return: 返回配置值
        '''
        # 直接调用get_section_for_data方法，固定section为'api_envi'
        return self.get_section_for_data('api_envi', option)


# 当这个文件被直接运行时执行的代码（模块测试代码）
if __name__ == '__main__':
    # 创建OperationConfig实例，使用默认配置路径
    oper = OperationConfig()
    # 获取[api_envi]节下的host配置并打印
    print(oper.get_envi('host'))
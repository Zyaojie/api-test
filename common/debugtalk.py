# -*- coding: utf-8 -*-
# @Time : 2025/5/1 21:32
# @Author : Zyaojie
# @File : debugtalk
# @Project : apitest
import random
from common.readyaml import ReadyamlData

class DeugTalk:

    def __init__(self):
        self.read = ReadyamlData()

    def get_extract_order_data(self,data,randoms):
        if randoms not in [0,-1,-2]:
            return data[randoms - 1]

    def get_extract_data(self,node_name,randoms = None):
        '''
        获取extract.yaml的数据
        :param node_name: extract.yaml中的key值
        :param randoms:随机读取extract.yaml的数据
        :return:
        '''
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms:self.get_extract_order_data(data,randoms),
                0: random.choice(data),
                -1: ','.join(data),
                -2: ','.join(data).split(',')
            }
            data = data_value[randoms]
        return data

    def md5_params(self,params):
        return 'ABCD123456' + str(params)

if __name__ == '__main__':

    debug = DeugTalk()
    print(debug.get_extract_data('product_id',-2))
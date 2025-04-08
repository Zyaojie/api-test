import requests


class SendRequests:
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
        else:
            res = requests.get(url=url, params=data, headers=header)
        return res.json()

    def post(self, url, data, header):
        """
        封装post请求
        :param url: 请求地址
        :param data: 请求参数
        :param header: 请求头
        :return:
        """
        if header is None:
            res = requests.post(url, data,verify=False)
        else:
            res = requests.post(url, data, headers=header,verify=False)
        return res.json()

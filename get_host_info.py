import requests
import json

conn_dic = {
    'pro_zabbix': {
        'url': 'http://xx.xx.xx.xx:xx/api_jsonrpc.php',
        'user': 'admin',
        'password': '111111'
    },
    'dev_zabbix': {
        'url': 'http://xx.xx.xx.xx:xx/zabbix/api_jsonrpc.php',
        'user': 'admin',
        'password': '111111'
    },
    'test_zabbix': {
        'url': 'xx.xx.xx.xx:xx/api_jsonrpc.php',
        'user': 'admin',
        'password': '111111'
    }
}


class ZabbixAPI():
    def __init__(self, conn_dic):
        self.__url = conn_dic.get('url')
        self.__user = conn_dic.get('user')
        self.__password = conn_dic.get('password')
        self.__header = {"Content-Type": "application/json-rpc"}
        self.__token_id = self.UserLogin()

    def UserLogin(self):
        """
        登录
        :return: 登录后的token
        """
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.__user,
                "password": self.__password
            },
            "id": 1,
        }
        return self.PostRequest(data)

    def PostRequest(self, data):
        """
        :param data: 传入josn结构参数，内容参考 get_host_info()函数中
        :return: 返回josn结构结果
        """
        result = requests.post(self.__url, data=json.dumps(data).encode('utf-8'), headers=self.__header)
        response = result.json()
        return response['result']

    def get_host_info(self):
        """
        :return: json结构查询结果数据
        """
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "host",
                ],
                "selectInterfaces": [
                    "ip"
                ]
            },
            "auth": self.__token_id,
            "id": 0
        }

        return self.PostRequest(data)


ip_list = []


def start():
    for key in conn_dic:
        zabbix_info = conn_dic[key]
        for host in ZabbixAPI(zabbix_info).get_host_info():
            ip = host['interfaces'][0]['ip']
            ip_list.append(ip)
    return ip_list

print(start())
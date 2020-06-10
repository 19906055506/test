# -*- coding: UTF-8 –*-
import requests
import time
import hashlib
import json
import ssl
import pymongo
import param as param

ssl._create_default_https_context = ssl._create_unverified_context
proxy_username = param.proxy_username  # 代理帐号名称,非用户名
proxy_passwd = param.proxy_passwd  # 代理帐号密码
proxy_server = param.proxy_server  # 代理服务器
pattern = 'json'  # API访问返回信息格式：json和text可选
num = 1  # 获取代理端口数量
test_num = 1  # 测试次数

key_name = 'user_name='
key_timestamp = 'timestamp='
key_md5 = 'md5='
key_pattern = 'pattern='
key_num = 'number='
key_port = 'port='


# 返回当前时间戳（单位为 ms）
def get_timestamp():
    timestamp = round(time.time() * 1000)
    return timestamp


# 进行md5加密
def get_md5_str(s):
    return hashlib.md5(bytes(s.encode('utf-8'))).hexdigest()


# 返回请求分配代理端口URL链接
def get_open_url():
    time_stamp = get_timestamp()
    md5_str = get_md5_str(proxy_username + proxy_passwd + str(time_stamp))
    return 'http://' + proxy_server + ':' \
           + '88' + '/open?' + key_name + proxy_username + \
           '&' + key_timestamp + str(time_stamp) + \
           '&' + key_md5 + md5_str + \
           '&' + key_pattern + pattern + \
           '&' + key_num + str(num)


# 返回重置本用户已使用ip URL链接
def get_reset_url():
    time_stamp = get_timestamp()
    md5_str = get_md5_str(proxy_username + proxy_passwd + str(time_stamp))
    return 'http://' + proxy_server + ':' \
           + '88' + '/reset_ip?' + key_name + proxy_username + \
           '&' + key_timestamp + str(time_stamp) + \
           '&' + key_md5 + md5_str + \
           '&' + key_pattern + pattern


# 使用代理进行测试 url为使用代理访问的链接，auth_port为代理端口
def testing(url, auth_port):
    proxies = {'http': "http://" + proxy_server + ':' + auth_port,
               'https': 'https://' + proxy_server + ':' + auth_port}
    try:
        # s.proxies.update(proxies)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
        }
        ret = requests.get(url, headers=header, proxies=proxies, timeout=5)
        print(ret.text)
        msg = str(ret.status_code)
    except Exception as e:
        msg = repr(e)
        print(msg)
    return msg


def updateProxy():
    client = pymongo.MongoClient(host=param.dbip, port=param.dbport)
    db = client[param.dbName]
    tbproxy = db[param.tbproxy]

    url_proxyfy = requests.get(get_open_url(), timeout=5)
    r = json.loads(url_proxyfy.text)
    r['timestamp'] = int(time.time())
    if r['code'] == 100:
        tbproxy.delete_many({})
        tbproxy.insert_one(r)
        s = '{}:{} 剩余ip数量:{}'.format(r['domain'], r['port'][0], r['left_ip'])
        print(s)
        return r
    else:
        updateProxy()


def getProxy():
    client = pymongo.MongoClient(host=param.dbip, port=param.dbport)
    db = client[param.dbName]
    tbproxy = db[param.tbproxy]
    r = tbproxy.find_one({}, {'domain': 1, 'port': 1, 'timestamp': 1, 'left_ip': 1})
    if int(time.time() - r['timestamp']) >= 3 * 60:
        return updateProxy()
    else:
        s = '{}:{} 剩余{}s, 剩余ip数量:{}'.format(r['domain'], r['port'][0], 3 * 60 - int(time.time() - r['timestamp']),
                                            r['left_ip'])
        print(s)
        return r


# def getProxy():
#     client = pymongo.MongoClient(host='localhost', port=27017)
#     db = client['testdb']
#     tbproxy = db['proxy']
#     r = tbproxy.find_one({}, {'timestamp'})
#     if int(time.time() - r['timestamp']) >= 3 * 60:
#         url_proxyfy = requests.get(get_open_url())
#         r = json.loads(url_proxyfy.text)
#         r['timestamp'] = int(time.time())
#         if r['code'] == 100:
#             tbproxy.delete_many({})
#             tbproxy.insert_one(r)
#             r = tbproxy.find_one({}, {'domain': 1, 'port': 1, 'timestamp': 1, 'left_ip': 1})
#             s = '{}:{} 剩余ip数量:{}'.format(r['domain'], r['port'][0], r['left_ip'])
#             print(s)
#             return r
#
#     else:
#         r = tbproxy.find_one({}, {'domain': 1, 'port': 1, 'timestamp': 1, 'left_ip': 1})
#         s = '{}:{} 剩余{}s, 剩余ip数量:{}'.format(r['domain'], r['port'][0], 3 * 60 - int(time.time() - r['timestamp']),
#                                             r['left_ip'])
#         print(s)
#         return r


# 实例简单演示如何正确获取代理端口，使用代理服务测试访问https://myip.ipip.net，验证后释放代理端口
if __name__ == '__main__':
    port = ''
    # 测试访问链接
    test_url = 'https://myip.ipip.net'  # 使用代理ip访问的网址,可自定义
    for count in range(test_num):
        try:
            open_url = get_open_url()
            r = requests.get(open_url, timeout=5)
            result = str(r.text)
            print(result)
            json_obj = json.loads(result)
            code = json_obj['code']
            if json_obj['code'] == 108:
                reset_url = get_reset_url()
                r = requests.get(reset_url, timeout=5)
            elif json_obj['code'] == 100:
                port = str(json_obj['port'][0])
                tmp = testing(test_url, port)
        except Exception as e:
            print(repr(e))
            continue

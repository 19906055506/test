import functools

from selenium.webdriver.chrome.options import Options
from flask import Response, jsonify
import www.proxyfy as proxyfy
import requests, random, time, os, sys
import param
from pynput.mouse import Controller, Button


def requestPy(url, headers={}, params={}, timeout=5):
    myproxy = proxyfy.getProxy()
    proxies = {
        'http': 'https://' + myproxy['domain'] + ':' + str(myproxy['port'][0]),
        'https': 'https://' + myproxy['domain'] + ':' + str(myproxy['port'][0]),
    }
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

    try:
        res = requests.get(url, headers=headers, proxies=proxies, params=params, timeout=timeout)
        return res
    except TimeoutError as e:
        print(TimeoutError, e)
    except requests.exceptions.ProxyError as e:
        proxyfy.updateProxy()


def getUseAgent():
    list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        # 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        # 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        # 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        # 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
        # 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
        # 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)',
        # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1) ',
        # 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
        # 'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
        # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
        # 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
        # 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
        # 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
        # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
        # 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'
    ]
    return random.choice(list)


def getHeadLess():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    return chrome_options


def clearLog():
    with open('../all.log', 'w', encoding='utf-8') as f:
        f.write('')


def clickTwice():
    mouse = Controller()
    mouse.click(Button.left)
    time.sleep(0.15)
    mouse.click(Button.left)


def token_baidu():
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        param.baidu_ak, param.baidu_sk)
    response = requests.get(url)
    if response:
        return response.json()


def getRootPath():
    rootPath = os.path.dirname(os.path.abspath(__file__))
    rootPath = os.path.dirname(rootPath)
    return rootPath


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, envirson=None):
        if isinstance(response, dict):  # 判断返回类型是否是字典(JSON)
            response = jsonify(response)  # 转换
        return super().force_type(response, envirson)


def log_excute_time(func):
    # decorator 用于计算函数执行时间
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('{} 执行结束 {:.8f} s'.format(func.__name__, time.time() - start))
        return res

    return wrapper
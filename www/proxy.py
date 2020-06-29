import requests, json, pymongo, datetime, time, param
import www.util as util
from www.log import log

mgclient = pymongo.MongoClient(host=param.mgdbip, port=param.mgdbport)
mgdb = mgclient[param.mgdbName]
tbproxy = mgdb[param.tbproxy]


def updateProxy():
    url = 'https://too.ueuz.com/frontapi/public/http/get_ip/index'
    params = {
        'type': -1,  # type提取方式-1(按次提取)，套餐提取请购买套餐
        'iptimelong': 1,  # iptimelongIP时长1(5分钟) 2(25分钟) 8(1分钟) 9(3分钟)
        'ipcount': 1,  # ipcount提取数量1-200
        'protocol': 0,  # protocol协议类型0(http/https) 1(socks5)
        'areatype': 1,  # areatype地区类型1(全国混拨),2(指定省份),3(指定城市)
        # area省份或城市代码见文本(因运营商限制,地区数据有可能存在不准确的情况,请酌情使用)
        'resulttype': 'json',  # resulttype数据格式3(txt) json(json)
        'duplicate': 0,  # duplicate去重周期0(不去重) 1(日去重) 2(周去重)
        'separator': 1,  # separator分隔符1(\r\n) 2(\b\r) 3(\r) 4(\n) 5(\t)(other:其他分隔符)
        'show_city': 0,  # show_city是否显示城市0(不显示) true(显示)
        'show_carrier': 0,  # show_carrier是否显示运营商0(不显示) true(显示)
        'show_expire': 1,  # show_expire是否显示有效期0(不显示) true(显示)
        'isp': -1,  # show_public_ip是否显示出口IP1(显示)
        # auth_key验证请在网站生成链接,复制此参数可以一直重复使用
        'auth_key': param.yz_auth_key,
    }
    response = requests.post(url, params=params, timeout=5).json()
    for i in response:
        s = {
            'domain': i['domain'],
            'port': i['ip_port'],
            'timestamp': int(datetime.datetime.strptime(i['expire_time'], '%Y-%m-%d %H:%M:%S').timestamp())
        }
        tbproxy.insert_one(s)


def getProxy():
    p = tbproxy.find()
    try:
        if time.time() >= int(p[0]['timestamp']):
            log.info('更新proxy_ip')
            tbproxy.delete_many({})
            updateProxy()
            return getProxy()
    except IndexError as e:
        log.info('更新proxy_ip')
        updateProxy()
        return getProxy()

    s = []
    for i in p:
        s.append({
            'http': "http://" + i['domain'] + ':' + str(i['port']),
            'https': 'https://' + i['domain'] + ':' + str(i['port'])
        })
    return s[0]


def test():
    url = 'https://myip.ipip.net/'
    headers = {
        'User-Agent': util.getUseAgent()
    }
    response = requests.get(url, headers=headers, proxies=getProxy())
    print(response.text)

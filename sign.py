#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import requests
import json
import time
import os
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

session = requests.session()
headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://s.m.taobao.com/h5?q=%E6%8C%87%E7%94%B2%E5%88%80&search=%E6%8F%90%E4%BA%A4&tab=all',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'h5api.m.taobao.com'
    }

def get_m_h5_tk():
    token_url = "https://h5api.m.taobao.com/h5/mtop.taobao.wsearch.appsearch/1.0/?jsv=2.4.5&appKey=12574478&t=1557460210731&sign=4cad397dfb8f9455976a15b0a0c737b9&api=mtop.taobao.wsearch.appSearch&v=1.0&H5Request=true&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp6&data={}"
    session.get(token_url, headers=headers)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    print(html_set_cookie)
    #"{'_m_h5_tk_enc': '9892c6f2340c27da4a11e6f5c7aa72e7', '_m_h5_tk': 'd655f00ac54282e4d01bc6c49a3d8cfd_1556625593335'}"
    return html_set_cookie

# 获取秘钥
def get_sign(data):
    #t = str(int(time.time() * 1000))
    t = "1557496164805"
    appkey = "12574478"
    set_cookie = get_m_h5_tk()
    #token = set_cookie["_m_h5_tk"].split("_")[0]
    #print(token)
    token = "4d14c10a29d9f4b8e45367aa9dbbf618"
    sign = hashlib.md5()
    datas = token + '&' + t + '&' + appkey + '&' + data
    sign.update(datas.encode())
    signs = sign.hexdigest()
    return signs, t

# 写入文件
def writeFile(filePath,jsonInfo):
    try:
        with open(filePath + str(int(time.time())) + ".json", "w") as jsonfile:
            json.dump(jsonInfo,jsonfile)
            jsonfile.close()
    except Exception as err:
        print(str(filePath) + "写入失败！")

if __name__ == "__main__":
    data = '{"q":"blackberry","search":"提交","tab":"all","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"58","wlsort":"58","page":1}'
    sign,t = get_sign(data)
    print(sign)
    print(t)

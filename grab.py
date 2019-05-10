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
from urllib import quote

# 这是新的方法，获取详情页的信息需要如下网址参考
session = requests.session()
headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=099d87ed80b8f819245aee821810d220&keyword=%E7%BE%8E%E9%A3%9F&page=0',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
        'host': 'h5api.m.taobao.com'
    }
def getJson(page, keyword):
    data = '{"q":"blackberry","search":"提交","tab":"all","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"58","wlsort":"58","page":1}'
    sign,t = get_sign(data)
    url =   'https://acs.m.taobao.com/h5/mtop.taobao.wsearch.h5search/1.0/?jsv=2.3.16&appKey=12574478&t='+ t +'&sign='+ sign +'&api=mtop.taobao.wsearch.h5search&v=1.0&H5Request=true&ecode=1&AntiCreep=true&AntiFlool=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data='+ quote(data)
    #print(url)
    r = session.get(url=url, headers=headers)
    html = r.text
    start = html.find('(')
    writeFile('./',json.loads(html[start + 1:-1]))
    #datas = (json.loads(html[start + 1:-1]))['result']['item']
    #totalPage = (json.loads(html[start + 1:-1]))['result']['totalPage']
    #return {"listItem":datas}


# 格式化字典
def formatDict(page, infoList):
    dictList = []
    for listItem in infoList:
        formatInfo = {}
        formatInfo["页数"] = page
        Trys("商品标题", "TITLE", formatInfo, listItem)
        Trys("原价", "GOODSPRICE", formatInfo, listItem)
        Trys("折扣价", "PROMOTEPRICE", formatInfo, listItem)
        Trys("售出件数", "SELL", formatInfo, listItem)
        Trys("详情页", "EURL", formatInfo, listItem)
        Trys("图像URL", "TBGOODSLINK", formatInfo, listItem)
        dictList.append(formatInfo)
    return dictList

def get_m_h5_tk():
    token_url = "https://h5api.m.taobao.com/h5/mtop.taobao.wsearch.appsearch/1.0/?jsv=2.4.5&appKey=12574478&t=1557460210731&sign=4cad397dfb8f9455976a15b0a0c737b9&api=mtop.taobao.wsearch.appSearch&v=1.0&H5Request=true&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp6&data={}"
    session.get(token_url, headers=headers)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    #print(html_set_cookie)
    #"{'_m_h5_tk_enc': '9892c6f2340c27da4a11e6f5c7aa72e7', '_m_h5_tk': 'd655f00ac54282e4d01bc6c49a3d8cfd_1556625593335'}"
    return html_set_cookie

# 获取秘钥
def get_sign(data):
    t = str(int(time.time() * 1000))
    #t = "1557496164805"
    appkey = "12574478"
    set_cookie = get_m_h5_tk()
    token = set_cookie["_m_h5_tk"].split("_")[0]
    #print(token)
    #token = "4d14c10a29d9f4b8e45367aa9dbbf618"
    sign = hashlib.md5()
    datas = token + '&' + t + '&' + appkey + '&' + data
    sign.update(datas.encode())
    signs = sign.hexdigest()
    return signs, t

# 一个try
def Trys(key1, key2, dict1, dict2):
    try:
        dict1[key1] = dict2[key2]
    except:
        dict1[key1] = "None"

    return dict1


# 创建递归文件夹
def createfiles(filepathname):
    try:
        os.makedirs(filepathname)
    except Exception as err:
        print(str(filepathname) + "已经存在！")

# 写入文件
def writeFile(filePath,jsonInfo):
    try:
        with open(filePath + str(int(time.time())) + ".json", "w") as jsonfile:
            json.dump(jsonInfo,jsonfile)
            jsonfile.close()
    except Exception as err:
        print(str(filePath) + "写入失败！")

def getJsonData(page, keyword):
    for item in range(0, page):
        jsonInfo = getJson(page + 1, keyword)
        # 保存json到本地
        filePath = "json/" + str(time.strftime('%Y%m%d', time.localtime(time.time()))) + "/"
        createfiles(filePath)
        with open(filePath + str(int(time.time())) + ".json", "w") as jsonfile:
            json.dump(jsonInfo,jsonfile)
            jsonfile.close()
        time.sleep(5)

if __name__ == "__main__":
    page = 1
    keyword = "blackberry".replace(" ", "+")
    getJsonData(page, keyword)

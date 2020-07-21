#!/usr/bin/python3
import requests
import time
import re
import sys
import hashlib
import random


session = requests.session()
def youdao_fanyi(name='test', to='AUTO'):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'user-agent': '5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'Referer': 'http://fanyi.youdao.com/',
    }
    ts = str(time.time()*1000)[:13]
    salt = ts + str(int(random.random() * 10))
    bv = hashlib.md5(
        headers['user-agent'].encode(encoding='UTF-8')).hexdigest()
    sign = hashlib.md5(
        f"fanyideskweb{name}{salt}Nw(nmmbP%A-r6U3EUn]Aj".encode(encoding='utf-8')).hexdigest()

    data = {
        'i': name,
        'from': 'AUTO',
        'to': to,
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,
        'sign': sign,
        'ts': ts,
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
    }
    session.post('http://fanyi.youdao.com/', headers=headers)
    try:
        return session.post(url, headers=headers, data=data).json()["translateResult"][0][0]['tgt']
    except:
        return session.post(url, headers=headers, data=data).text
help = {
    "中文": "zh-CHS",
    "英语": "en",
    "韩语": "ko",
    "日语": "ja",
    "法语": "fr",
    "俄语": "ru",
    "西班牙语": "es",
    "葡萄牙语": "pt",
    "印地语": "hi",
    "阿拉伯语": "ar",
    "丹麦语": "da",
    "德语": "de",
    "希腊语": "el",
    "芬兰语": "fi",
    "意大利语": "it",
    "马来语": "ms",
    "越南语": "vi",
    "印尼语": "id"
}
if __name__ == '__main__':
    lists = ''
    for i in sys.argv[1:]:
        if i.lower() == '--help':
            input(help)
            break
        lists += i + ' '
    if lists:
        lists = lists[:-1]
        requests = youdao_fanyi(lists)
    else:
        requests = youdao_fanyi(input('请输入要翻译的文字：'))
    print(requests)
    while True:
        requests = youdao_fanyi(input('\n请输入要翻译的文字：'))
        print(requests)

# -*- coding: utf-8 -*-
import fileinput
import json
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
from scrapy import Selector
from scrapy.log import logger
from dianping_pro.config import FONT_CACHE_FILE,woff_string


def filter_tags(htmlstr):
    soup = BeautifulSoup(htmlstr, "lxml")
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]
    return soup.text


def get_dianping_cookies():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    while True:
        try:
            r = requests.get("http://www.dianping.com", headers=headers)
            break
        except requests.exceptions.ConnectTimeout:
            time.sleep(2)
            continue
        except requests.exceptions.Timeout:
            time.sleep(2)
            continue
        except Exception as e:
            print(e), 'error'
            time.sleep(2)
            continue
    _cookie = {}
    for cookie in r.cookies:
        _cookie[cookie.name] = cookie.value
    return (_cookie)



def to_base36(value):
    """
    将10进制整数转换为36进制字符串
    """
    if not isinstance(value, int):
        raise TypeError(
            "expected int, got %s: %r" %
            (value.__class__.__name__, value))
    if value == 0:
        return "0"
    if value < 0:
        sign = "-"
        value = -value
    else:
        sign = ""

    result = []
    while value:
        value, mod = divmod(value, 36)
        result.append("0123456789abcdefghijklmnopqrstuvwxyz"[mod])
    return sign + "".join(reversed(result))


def decode_poi(C):
    """
    解析大众点评POI参数
    """
    digi = 16
    add = 10
    plus = 7
    cha = 36
    I = -1
    H = 0
    B = ''
    J = len(C)
    G = ord(C[-1])
    C = C[:-1]
    J -= 1

    for E in range(J):
        D = int(C[E], cha) - add
        if D >= add:
            D = D - plus
        B += to_base36(D)
        if D > H:
            I = E
            H = D

    A = int(B[:I], digi)
    F = int(B[I + 1:], digi)
    L = (A + F - int(G)) / 2
    K = float(F - L) / 100000
    L = float(L) / 100000
    return {'lat': K, 'lng': L}


# def read_cache():
#     """
#     #从文件读取解码的缓存dict
#     :return:
#     """
#     logger.info('读入所有缓存字体')
#     file_exist = os.path.exists(FONT_CACHE_FILE)
#     if not file_exist:
#         with open(FONT_CACHE_FILE, 'w') as fw:
#             fw.write(json.dumps({}))
#             return
#     with open(FONT_CACHE_FILE, 'r') as f4:
#         data = f4.readline()
#         if not data:
#             return
#         data = json.loads(data)
#         return data

def write_file(url,model):
    css_url = 'http:' + url
    print(css_url)
    for _ in range(20):
        try:
            css_resp = requests.get(url=css_url, timeout=5)
            break
        except requests.exceptions.ConnectTimeout:
            time.sleep(2)
            continue
        except requests.exceptions.Timeout:
            time.sleep(2)
            continue
        except Exception as e:
            print(e), 'error'
            time.sleep(2)
            continue

    css_text = css_resp.text
    if model == 'wb':
        css_text = css_resp.content
    with open(url[-10:],model) as f:
        f.write(css_text)

def get_all_path():
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    file_list = []
    for maindir, subdir, file_name_list in os.walk(parent_path):
        file_list+=file_name_list
    return file_list

def font_xml(font_url):
    font_file = font_url[-10:]
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    path = '{}/{}'.format(parent_path, font_file)
    font = TTFont(path)
    gly_list = font.getGlyphOrder()  # 获取 GlyphOrder 字段的值

    # for gly in gly_list[2:]:  # 前两个值不是我们要的，切片去掉
    #     print(gly)  # 打印

    font.saveXML('./' + font_file + '.xml')
    return  gly_list[2:]

def get_font_url(path,partten):
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)
    path = '{}/{}'.format(parent_path,path)
    with open(path,'r') as f:
        text =f.read()
    # print(partten)
    a = re.findall(r'url\("(//s3plus.meituan.net/v1/mss_\w+/font/\w+.woff)"\);\} \.'+(partten),text)
    if a:
        return a[0]


def get_woffs(woff_string):
    woffs = [i for i in woff_string if i != '\n' and i != ' ']
    return woffs


def convert_api(pattarn,tag_name,css_url):
    pattarn = 'uni'+repr(pattarn).strip("'")[-4:]
    pathes = get_all_path()
    # print(pathes)
    if css_url[-10:] not in pathes:
        write_file(css_url,'w')
    font_url = get_font_url(css_url[-10:], tag_name)
    if font_url[-10:] not in pathes:
        write_file(font_url,'wb')
    xml_tag_list = font_xml(font_url[-10:])
    # print(pattarn,xml_tag_list)
    if pattarn in xml_tag_list:
        p_index = xml_tag_list.index(pattarn)
        woffs = get_woffs(woff_string)
        print('{}>>{}'.format(pattarn,woffs[p_index]))
        return  woffs[p_index]
    else:
        logger.error('解析出错')

if __name__ == '__main__':

    a = '//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/3e0f85608a2fd2049cf15f6cbb3c4022.css'
    convert_api('\uf858', 'shopNum', a)
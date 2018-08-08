#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/8/8

# build-in
import time
import winreg
import subprocess
# third-part
import json
import requests
import lxml.html
import logging
# project

# 日志记录
logger = logging.getLogger('AutoClicker')
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
s_handler = logging.StreamHandler()
s_handler.setFormatter(fmt)
logger.addHandler(s_handler)

# 是否需要生成日志文件
f_handler = logging.FileHandler('AutoClicker.log')
f_handler.setFormatter(fmt)
logger.addHandler(f_handler)

# 注册表的信息
root = winreg.HKEY_CURRENT_USER
proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
sleep_time = 1 * 2


# IE 方法
def open_ie():
    # 开启IE
    cmd = [r'C:\Program Files\Internet Explorer\iexplore.exe',
           'http://www1.elecfans.com/www/delivery/myafr.php?target=_blank&cb=0.15074282898868696&zoneid=600']
    subprocess.Popen(cmd)
    # cmd = '"C:\\Program Files\\Internet Explorer\\iexplore.exe" http://www.elecfans.com/'
    # os.system(cmd)


def close_ie():
    # 关闭IE
    cmd = 'taskkill -f -t -im iexplore.exe'
    subprocess.Popen(cmd)


def restart_ie():
    close_ie()
    time.sleep(0.5)
    open_ie()


def init_proxy():
    proxy_enable = check_status()
    if proxy_enable:
        switch_ie_proxy('127.0.0.1:1080', switch=0)


def check_status():
    _Key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, proxy_path)
    _value, _type = winreg.QueryValueEx(_Key, "ProxyEnable")
    return True if _value else False


# 注册表方法
def switch_ie_proxy(proxy=None, switch=0):
    if proxy is None:
        return None

    # 代理的注册表键值
    kv = [
        (proxy_path, "ProxyEnable", switch, winreg.REG_DWORD),
        (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]

    for key_path, value_name, value, value_type in kv:
        _Key = winreg.CreateKey(root, key_path)
        winreg.SetValueEx(_Key, value_name, 0, value_type, value)


def get_proxy(limit_num=50):
    rs = requests.get("http://proxy.elecfans.net/proxys.php?key=AXw1KwWIsK&num={limit}".format(limit=limit_num))
    proxies = json.loads(rs.text.encode('utf-8'))
    servers = proxies.get('data', [])
    ip_list = []
    for info in servers:
        ip = info.get('ip', None)
        ip_list.append(ip)
    return ip_list


def check_proxy(proxy=None):
    proxies = {
        'http': 'http://{_proxy}'.format(_proxy=proxy),
        'https': 'http://{_proxy}'.format(_proxy=proxy)
    }
    logger.debug(u'测试代理 {0}'.format(proxy))
    url = 'http://www1.elecfans.com/www/delivery/myafr.php?target=_blank&cb=0.15074282898868696&zoneid=600'
    _headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
    }
    try:
        start_time = int(time.time())
        end_time = int(time.time())
        rs = requests.get(url=url, headers=_headers, proxies=proxies, timeout=15)
        # 判断是否200
        if rs.status_code == 200:
            # 判断内容是否正确
            if '400 Bad Request' in rs.text or 'Gateway Timeout' in rs.text:
                return None
            if 'database not access' in rs.text:
                return None
            if not rs.text.strip():
                return None
            if rs.text is None:
                return None
            # 判断是否能成功加载内容
            x = lxml.html.fromstring(rs.text)
            title = x.xpath('//title')
            title = title[0] if title else ''
            if '504' in title:
                return None
            ad_list = x.xpath('//ul[@id="ads_lists"]//li')
            if ad_list:
                end_time = int(time.time())
                load_time = end_time - start_time
                logger.debug(u'加载成功, 加载时长{0}！proxy {1}'.format(load_time, proxy))
                return proxy, load_time
            else:
                return None
                # return proxy if ad_list else None
        else:
            return None
    except requests.RequestException:
        return None


if __name__ == "__main__":
    # switch_ie_proxy('183.222.102.106:8080', switch=0)
    # print check_proxy('127.0.0.1:1080')
    # init_proxy()
    # while True:
    #     try:
    #         proxy_list = get_proxy(limit_num=3000)
    #         for ip in proxy_list:
    #             rst = check_proxy(ip)
    #             if rst is None:
    #                 continue
    #             _proxy, wait_load_time = rst
    #             logger.debug(u'使用代理 {ip}'.format(ip=_proxy))
    #             switch_ie_proxy(_proxy, switch=1)
    #             open_ie()
    #             logger.debug(u"等待页面加载 {0}s".format(wait_load_time + 2))
    #             time.sleep(wait_load_time + 2)
    #             # 启动广告点击脚本
    #             subprocess.call(r'C:\Users\Administrator\Desktop\run_auto\ad.exe')
    #             time.sleep(10)
    #             # 关闭代理
    #             switch_ie_proxy(_proxy, switch=0)
    #             close_ie()
    #     except Exception as e:
    #         print e
    proxy_list = get_proxy(limit_num=100)
    for ip in proxy_list:
        rst = check_proxy(ip)
        if rst is None:
            continue
        print(ip)
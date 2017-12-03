#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by VinChan on 12/3/2017 0003
import requests

order_detail = 'http://www.szlcsc.com/order/orderDetailList.html'
cookies = {
    'SESSION': '7819a2d6-8ebc-4b2f-ac00-35ef9fc78f44',
}
headers = {
    'Host': 'www.szlcsc.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.szlcsc.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'orderId': '1039906',
    'customerId': '493370',
}


def main():
    rs = requests.post(url=order_detail, data=data, headers=headers, cookies=cookies)
    print rs.content


if __name__ == "__main__":
    main()

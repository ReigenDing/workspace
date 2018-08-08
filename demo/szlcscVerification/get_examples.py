#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/9/28
import requests
import config
import time


def main():
    for x in range(20):
        rs = requests.get(url='http://www.szlcsc.com/jsp/pass/ip_image.jsp', headers=config.DEFAULT_HEADERS)
        time.sleep(1)
        with open('{0}.jpg'.format(x), 'wb') as fp:
            fp.write(rs.content)


if __name__ == '__main__':
    main()

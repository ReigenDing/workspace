#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/8/14

import time
import logging

logger = logging.getLogger('EXAMPLE')
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
s_handler = logging.StreamHandler()
s_handler.setFormatter(fmt)
logger.addHandler(s_handler)

# 是否需要生成日志文件
f_handler = logging.FileHandler('../logs/keep_alive_%s.log' % time.strftime("%Y-%m-%d_%H", time.localtime()))
f_handler.setFormatter(fmt)
logger.addHandler(f_handler)


def main():
    logger.debug('testing...')


if __name__ == '__main__':
    main()

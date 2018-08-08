# -*- coding: utf-8 -*
import os
import logging
import datetime
from logging.handlers import RotatingFileHandler


LOG_DIR = os.getcwd()
# GET LOGGER
FTP_LOGGER = logging.getLogger("fpt_logger")
FMT = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
# 文件handler
FILE_HANDLER = RotatingFileHandler(filename=os.path.join(LOG_DIR, 'ftp_{d}.logs'.format(d=datetime.datetime.now().strftime("%Y-%m-%d_%H"))), mode='a+')
# 控制台handler
CONSOLE_HANDLER = logging.StreamHandler()
# handler加载format
FILE_HANDLER.setFormatter(FMT)
CONSOLE_HANDLER.setFormatter(FMT)
# 添加handler到logger
FTP_LOGGER.addHandler(FILE_HANDLER)
FTP_LOGGER.addHandler(CONSOLE_HANDLER)
# 设置日志输出等级
FTP_LOGGER.setLevel(logging.DEBUG)


if __name__ == '__main__':
    FTP_LOGGER.info("hello world!")

# -*- coding:utf-8 -*-
# !/usr/bin/python

import os
import logging
from tqdm import tqdm
import time
import threading
from zipfile import ZipFile
from ftplib import FTP

unzip_logger = logging.getLogger('unzip_logger')
unzip_logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')
console_handler = logging.StreamHandler()
console_handler.setFormatter(fmt)
unzip_logger.addHandler(console_handler)


def unzip_file(zip_list, target_dir):
    zip_list = zip_list if zip_list else []
    target_dir = target_dir if target_dir else os.getcwd()
    for zip_file_path in zip_list:
        if not os.path.isfile(zip_file_path) and os.path.splitext(zip_file_path)[-1] != '.zip':
            unzip_logger.log(logging.WARNING, "{0} is not a  zip file! check your file path!".format(zip_file_path))
            continue
        with ZipFile(file=zip_file_path) as zip_fp:
            unzip_logger.info("unzip files to {0}".format(target_dir))
            show_the_bar = threading.Thread(target=progress_bar, args=(target_dir, zip_fp.infolist()))
            show_the_bar.start()
            zip_fp.extractall(target_dir)
            show_the_bar.join()


def progress_bar(target_dir, files_info):
    while True:
        break_the_loop = True
        for file in [f for f in files_info if hasattr(f, 'file_size')]:
            file_path = os.path.join(target_dir, file.filename)
            if os.path.exists(file_path):
                with tqdm(total=file.file_size) as bar:
                    while True:
                        extracted_size = os.path.getsize(file_path)
                        bar.update(extracted_size)
                        if extracted_size == file.file_size:
                            break
            else:
                break_the_loop = False
        if break_the_loop:
            break


if __name__ == '__main__':
    # file_list = [r'F:\Downloads\Compressed\jieba-master.zip']
    # unzip_file(file_list, r'F:\Share')
    # for x, y, z in os.walk(r'D:\AppDocuments\NetSarang Computer\6\Xshell\Sessions'):
    #     print(x)
    #     print(y)
    #     print(z)
    # a = FTP()
    # a.retrlines()
    unzip_logger.info("hello world!")

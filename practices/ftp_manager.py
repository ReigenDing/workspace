# -*- coding:utf-8 -*-
# !/usr/bin/python
import os

FTP_HOST = ''
FTP_USERNAME = 'vin'
FTP_PASSWORD = 'Aa111111'

FTP_AUTO_DOWNLOAD_SCRIPT = """HOST={ftp_host}
USER={user}
PASSWORD={password}
ftp -n -v $HOST << EOT
user $USER $PASSWORD
ls -la
bye
EOT""".format(ftp_host=FTP_HOST, user=FTP_USERNAME, password=FTP_PASSWORD)


def auto_upload():
    # target_path = target_path if target_path else '/'
    # if not file_name:
    #     print('Please set up the file name which you want tu upload.')
    #     return 0
    print(os.popen(FTP_AUTO_DOWNLOAD_SCRIPT).read())


if __name__ == '__main__':
    auto_upload()

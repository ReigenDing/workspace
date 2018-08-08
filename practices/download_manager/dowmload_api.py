#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests

from download_manager import DEFAULT_DOWNLOAD_HEADERS


# get file info
def _get_file_info_from_remote_server(url, **kwargs):
    timeout = kwargs.get('timeout', 20)
    proxies = kwargs.get('proxies', None)
    try:
        file_headers = requests.head(url=url, headers=DEFAULT_DOWNLOAD_HEADERS, timeout=timeout, proxies=proxies)
    except requests.RequestException:
        return {}
    file_info = {}
    if 'Content-Disposition' in file_headers.headers.keys():
        content_disposition = file_headers.headers.get('Content-Disposition')
        if 'attachment' in content_disposition:
            match_file_name = re.search(r'filename="|\'([^"\']*)"|\'')
            file_name = match_file_name.group(1) if match_file_name else ''
            file_info.update({
                'file_name': file_name,
            })
        elif 'form-data' in content_disposition:
            match_form_data = re.findall(r'(\s*[^=]+=([^;]+);)', content_disposition)
            for k, v in match_form_data:
                file_info.update({k: v})
        else:
            return {}
    if 'Content-Length' in file_headers.headers.keys():
        content_length = file_headers.headers.get('Content-Length', '')
        content_length = int(content_length) if content_length.isdigit() else 0
        file_info.update({
            'file_size': "{0} Mb".format(content_length / 1024.0 if content_length > 1024 else content_length),
        })
    return file_info


def main():
    pass


if __name__ == '__main__':
    main()

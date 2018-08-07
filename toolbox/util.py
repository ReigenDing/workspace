# -*- coding: utf-8 -*
import os
import logging
import datetime

from logging.handlers import RotatingFileHandler
from sshtunnel import SSHTunnelForwarder


def get_default_logger(logger_name="default_logger", logging_level=logging.DEBUG, log_file=False, **kwargs):
    """获取一个默认设置好的日志对象default_logger
    默认向控制台输出，日志输出级别为DEBUG，日志文件默认目录为脚本执行的当前目录，日志文件功能默认是关闭状态，
    日志文件按小时切片。可以通过传入参数 filename 设置日志文件路径， maxBytes 设置日志文件分片大小。
    :param logger_name: 定义logger名，默认值为 default_logger
    :param logging_level: 定义日志输出级别，默认值为 logging.DEBUG
    :param log_file: 是否启用日志文件，默认为 False，开启后可以传入参数 filename 和 maxBytes
    :param kwargs: {'filename': 日志文件的路径, 'maxBytes': 日志文件分片的大小}
    :return: logger object
    """
    # GET LOGGER
    default_logger = logging.getLogger(logger_name)
    default_logger.setLevel(logging_level)
    # 默认输出格式
    fmt = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', '%Y-%m-%d %H:%M:%S')

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)
    default_logger.addHandler(console_handler)
    # 文件输出，默认是关闭的
    if log_file:
        default_filename = os.path.join(os.getcwd(),
                                        'default_{dt}.logs'.format(dt=datetime.datetime.now().strftime("%Y-%m-%d_%H")))
        file_handler = RotatingFileHandler(filename=kwargs.get('filename', default_filename), mode='a+',
                                           maxBytes=kwargs.get('maxBytes', 0))
        file_handler.setFormatter(fmt)
        default_logger.addHandler(file_handler)
    return default_logger


def get_ssh_tunnel(*args, **kwargs):
    """建立ssh隧道连接远程服务器
    例如建立连接 TIDB 的ssh隧道可以使用, 传入参数
    {"ssh_address_or_host": ("30.16.47.238", 80)
    "ssh_username": root,
    "ssh_password": password,
    "remote_bind_address": ("30.18.104.33", 4000),}
    使用时需要自己维护隧道的连接状态， ssh_tunnel.start(), ssh_tunnel.close()
    :return: ssh隧道对象，映射到本地端口号
    """
    ssh_tunnel = SSHTunnelForwarder(*args, **kwargs)
    return ssh_tunnel, ssh_tunnel.local_bind_port


if __name__ == '__main__':
    # 测试日志方法
    logger = get_default_logger(log_file=True)
    logger.info("hello world!")

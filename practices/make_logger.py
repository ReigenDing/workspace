# -*- coding: utf-8 -*
import os
import logging
import datetime
from logging.handlers import RotatingFileHandler


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


if __name__ == '__main__':
    logger = get_default_logger()
    logger.info("hello")

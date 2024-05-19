###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      history_update
#   Creat_time:     2024/5/19   10:18
#   Author:         富视投资 
#   Description:
###########################################################################
import json
import os

import pandas as pd

from beehive.common import get_function_parameters, get_function_name, check_symbols
from beehive.history_load import load_history
from beehive.history_update import update_history


def get_history(symbols=None, period='d', start=None, end=None,
                fields="datetime,open,close,high,low,volume,turnover",
                adjust='-1', spider: object = None,
                update=True, path=None, data_style='csv'
                ):
    """
    从网上下载股票历史k线
    :param symbols:     股票代码    str格式，多个以,分隔，支持list、tuple,    None为全市场
    :param period:      k线周期，   str格式，d日 m月 w周 s季 y年 5分钟
    :param start:       开始日期    str格式，'20010203'                    None为最早日期
    :param end:         结束日期    str格式，'20240511'                    None为今天
    :param fields:      k线字段    str格式，默认包含7条
    :param adjust:      复权       str格式，-1前、0不、1后              默认前复权 -1
    :param spider:        来源网站    数据采集类 对象
    :param update:      是否从网上更新     默认是
    :param path:        如果update为False path为本地读取路径 如果update为True path为本地存储路径
    :param data_style:  存储的数据类型 默认是csv
    :return:   字典
                    {'600847':
                            [
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9],
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9],
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9]
                            ],
                    '000520':
                            [
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9],
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9],
                                ['20010203', 5.62, 5.88, 5.99, 5.55, 123456, 9.9]
                            ],
                    ... ...
                    }
    """

    # 本函数的所有形参
    args, kwargs = get_function_parameters(eval(get_function_name()))

    # 把实参赋值给形参 kwargs['symbols'] = symbols
    for key, value in kwargs.items():
        kwargs[key] = eval(key)
    # 检查symbols############################### 是否剔除指数票 ####################################
    if kwargs.get('symbols') is None:
        """获取股票代码"""
        print(f"symbols为None,{get_function_name()}:{__file__}")
        with open("E://abcd.txt", 'r') as f:
            symbols = json.load(f)['stock'][:10]
    # 更新实参
    kwargs.update({'symbols': symbols})

    # 如果指定从网上下载
    if update:
        return update_history(*args, **kwargs)

    # 本地读取
    return load_history(*args, **kwargs)


"""
    # 全市场 日k线 不存储
    get_history()

    # 带存储
    get_history(symbols='600848,000520', path="E://datas")

    # 本地读取
    get_history('600848,000520', update=False, path="E://datas")

    # 其他symbols格式
    get_history(symbols=['600848', '000520'])
"""

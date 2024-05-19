###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      history_load
#   Creat_time:     2024/5/19   20:39
#   Author:         富视投资 
#   Description:
###########################################################################
import os

import pandas as pd

from beehive.common import check_symbols


def load_history(*args, **kwargs):
    """ 本地读取历史数据
    1,不指定path 不指定symbols
    2，不指定path，指定symbols
    3，指定path，不指定symbols
    4，指定path，指定symbols
    """
    # 路径(文件或者文件夹)
    path = kwargs.get('path', None)
    # 股票代码
    symbols = kwargs.get('symbols', None)
    # 日线
    period = kwargs.get('period', 'd')

    # 只要指定了symbols 就得检查其类型
    if symbols is not None:
        # 检查symbols是否list
        symbols = check_symbols(symbols)

    # 期待的结果
    results_dict = dict()
    # 如果未指定path
    if path is None:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'datas/history/' + period)
        # 如果symbols=None 则为全市场股票代码
        if symbols is None:
            # 遍历文件夹下的所有文件
            for root, folder, filenames in os.walk(path):
                symbols_file_list = [os.path.join(root, filename) for filename in filenames]
            results_dict = {os.path.basename(filename)[:6]: pd.read_csv(filename) for filename in symbols_file_list}
        else:
            # 获取本包内历史数据的存储目录
            results_dict.update({symbol: pd.read_csv(os.path.join(path, symbol + '.csv')) for symbol in symbols})
    else:  # 如果指定了path
        if symbols is None:  # 未指定symbols
            # 判断path是文件
            if os.path.isfile(path):
                results_dict = {os.path.basename(path)[:6]: pd.read_csv(path)}
            if os.path.isdir(path):
                # 遍历文件夹下的所有文件
                for root, folder, filenames in os.walk(path):
                    symbols_file_list = [os.path.join(root, filename) for filename in filenames]
                results_dict = {os.path.basename(filename)[:6]: pd.read_csv(filename) for filename in symbols_file_list}
        else:  # 指定了symbols
            results_dict.update({symbol: pd.read_csv(os.path.join(path, symbol + '.csv')) for symbol in symbols})

    # 根据指定的列提取
    fields = kwargs.get('fields', 'datetime,open,close,high,low,volume,turnover')
    fields = fields.replace(' ', '').split(',')

    return {symbol: result[fields] for symbol, result in results_dict.items()}
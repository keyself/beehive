###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      easthistory
#   Creat_time:     2024/5/19   13:22
#   Author:         富视投资 
#   Description:
###########################################################################
import datetime
import json
import time

import pandas as pd
from jsonpath import jsonpath

from beehive.base_history import HistoryBase
from beehive.common import check_symbols


class EastHistory(HistoryBase):
    """东财 历史数据类 ：抽象基类的具体实现类
    注意:
        self._symbols是原始股票代码
        self.symbols是个性化股票代码

        指定请求头可以直接用self.url,self.headers而不必使用self._url
        请求url和请求头会自动更新，而不是新值

        从父类继承属性 self.args, self.kwargs, self.symbols等
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?'
        self.headers = {
            "Host": "push2his.eastmoney.com",
            'Referer': 'http://quote.eastmoney.com/'
        }

    def format_symbols(self):
        """个性化所有的股票代码"""
        return ["0." + symbol[-6:] if self.get_market(symbol) == "sz" else "1." + symbol[-6:] for symbol in
                self._symbols][:]

    def format_parameters(self, symbol) -> dict:
        """个性化处理请求参数"""
        # 发起请求前构造参数 批处理因子 和 参数的组合
        params = {
            'fields1': 'f2',
            # 'fields2': 'f51,f52,f53,f54,f55,f56,f61',
            'ut': '7eea3edcaed734bea9cbfc24409ed989',
            '_': str(time.time()),
        }
        # 对应关系
        pattern = {'d': '101',
                   'w': '102',
                   'm': '103',
                   's': '104',
                   'b': '105',
                   'y': '106',
                   '5': '5',
                   '15': '15',
                   '30': '30',
                   '60': '60',
                   }

        # 把传进来的参数转换为个性化的请求参数
        # 如 传进来的period='d'， 对应 klt=101
        params['klt'] = pattern[self.kwargs.get('period', 'd')]
        # 计算时间
        params['beg'] = self.kwargs.get('start', '0')
        if params['beg'] is None:
            params['beg'] = '0'

        end = self.kwargs.get('end', None)
        if end is None:
            today = datetime.date.today()
            end = datetime.datetime.strftime(today, '%Y%m%d')
        params['end'] = end

        # 股票代码
        params['secid'] = symbol

        # 是否复权
        adjust = self.kwargs.get('adjust', '1')
        if adjust is None:
            params['fqt'] = '1'
        elif adjust == '0':
            params['fqt'] = '0'
        elif adjust == '-1':
            params['fqt'] = '1'
        elif adjust == '1':
            params['fqt'] = '2'
        else:
            params['fqt'] = '1'

        # 对应关系
        fileds_pattern = {'datetime': 'f51',
                          'open': 'f52',
                          'close': 'f53',
                          'high': 'f54',
                          'low': 'f55',
                          'volume': 'f56',
                          'turnover': 'f61',
                          }
        params['fields2'] = ','.join([fileds_pattern[field] for field in self._fields])

        return params

    def process_single_response(self, symbol, raw_response) -> dict:
        """加工 单次请求得到的结果 """
        json_response = json.loads(raw_response)

        klines = jsonpath(json_response, "$..klines")

        if not klines or klines is None:
            return None

        klines = klines[0]
        # 统一转换为 df 格式
        line = [bar.split(',') for bar in klines]

        # fields = self.kwargs.get('fields', None)
        # if fields:
        #     fields = check_symbols(fields)
        #     if len(fields) < 7:
        #         fields = "datetime, open, close, high, low, volume, turnover".split(',')
        # else:
        #     fields = "datetime, open, close, high, low, volume, turnover".split(',')

        df = pd.DataFrame(
            data=line,
            index=None,
            columns=self._fields
        )

        # # 设置索引
        # df['datetime'] = pd.to_datetime(df['datetime'])
        # df.set_index('datetime', inplace=True)

        # fields = self.kwargs.get('fields', None)
        # if fields:
        #     fields = check_symbols(fields)
        # else:
        #     fields = "datetime, open, close, high, low, volume, turnover".replace(' ', '').split(',')
        # print(df.keys())
        return {symbol[-6:]: df}

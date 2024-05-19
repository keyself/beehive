###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      base_history
#   Creat_time:     2024/5/19   13:33
#   Author:         富视投资 
#   Description:
###########################################################################
import abc
import asyncio
import json
import os

import aiohttp

from beehive.common import check_symbols


class HistoryBase:
    """
    历史数据采集类的抽象基类：
        制定编程规则 子类按此编程 抽象基类不可实例化 具体实现类必须实现抽象方法
    """

    def __init__(self, *args, **kwargs):
        # 子类一经实例化就具有两个参数
        self.args = args
        self.kwargs = kwargs
        # 请求网址 头 参数 ，动态属性
        # 子类直接指定 self.url 而不必self._url
        self._url = ''
        self._headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/115.0.0.0 Safari/537.36',
            'accept': 'application/json',
        }
        # 要采集 的 股票代码
        # 如果为None则全市场，
        # 终端用户可能会直接调用update_history而不经过get_history，故多写了一遍
        symbols = self.kwargs.get('symbols', None)
        if symbols is None:
            print(f"symbols为None,{self.__class__.__name__}:{__file__}")
            with open("E://abcd.txt", 'r') as f:
                symbols = json.load(f)['stock']
        # 原始股票代码
        self._symbols = check_symbols(symbols)
        # 个性化代码
        self.symbols = self.format_symbols()

        # fields 创建df时列名会用 请求的参数计算会用 筛选数据返回时要用
        self._fields = self.kwargs.get('fields', 'datetime,open,close,high,low,volume,turnover')
        self._fields = self._fields.replace(' ', '').split(',')

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value_dict):
        self._headers.update(value_dict)

    def update(self):
        """对外接口：获取历史交易k线数据"""
        # 发给执行者 返回结果
        results_list = asyncio.run(self.create_and_execute_tasks())

        # 转字典格式 {代码: df}
        d = dict()
        for x in results_list:
            if x and x is not None:
                d.update(x)

        # 先看path是否指定， 再看path是否存在
        # 存储 如果指定了path的话
        path = self.kwargs.get('path', None)
        # 如果指定了path
        if path is not None:
            path = os.path.join(path, self.kwargs.get('period', 'd'))
            # 如果路径不存在则新建
            if not os.path.exists(path):
                os.makedirs(path)

            # 存储
            for symbol, df in d.items():
                file_name = os.path.join(path, symbol + '.csv')
                # print(f"即将保存：", file_name)
                df.to_csv(file_name, index=0)

        return d

    async def create_and_execute_tasks(self):
        """创建并执行 多携程任务"""
        # print("创建并执行 多携程任务", self.symbols)
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.single_request(session, symbol, identity=symbol)) for symbol in
                     self.symbols]
            return await asyncio.gather(*tasks)

    async def single_request(self, session, symbol, identity):
        # 发起请求前构造参数 批处理因子 和 参数的组合
        params = self.format_parameters(symbol)

        # 新建会话，使用会话发送请求
        async with session.get(self.url, params=params, headers=self.headers) as response:
            raw_response = await response.read()
            # print("处理采集到的结果", symbol)
            # 处理返回结果
            if response.status == 200:
                return self.process_single_response(symbol, raw_response)

    @abc.abstractmethod
    def process_single_response(self, symbol, raw_response) -> dict:
        """处理单次采集的结果"""
        pass

    @abc.abstractmethod
    def format_parameters(self, symbol) -> dict:
        """发起请求前构造参数 批处理因子 和 参数的组合"""
        pass

    @abc.abstractmethod
    def format_symbols(self):
        """个性化股票代码"""
        pass

    def get_market(self, symbol):
        """
            获取股票代码市场前缀
            （获取股票代码对应的证券市场，sh、sz）
        """
        # 断言
        assert type(symbol) is str, "symbol need str type"

        if symbol.startswith(('sh', 'sz', 'SH', 'SZ')):
            return symbol[:2]

        sh_head = ("50", "51", "60", "90", "110", "113", "118",
                   "132", "204", "5", "6", "9", "7")

        return 'sh' if symbol.startswith(sh_head) else 'sz'



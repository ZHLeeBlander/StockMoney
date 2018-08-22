#!/usr/bin/python
# -*- coding: utf-8 -*-

import tushare
import datetime
import time

class Stock():
    '''
    获取股票的实时信息
    '''
    def __init__(self, stock_num='10000'):
        self.stock_num = stock_num

    # def __init__(self, q, stock_num='10000'):
    #     self.q = q
    #     self.stock_num = stock_num
    #     self._terminal = True

    def query_stock_real_price(self):
        df = tushare.get_realtime_quotes(self.stock_num)
        df = df[['price', 'time']]
        price = df['price'].values[0]
        time = df['time'].values[0]
        return price, time

    def get_kline_data(self, ktype='ma5'):
        today = time.strftime("%Y-%m-%d", time.localtime())
        df = tushare.get_hist_data(self.stock_num, start='2018-8-16', end=today)
        print df[[ktype]]
        return (df[[ktype]])

    # def start_run(self):
    #     while self._terminal:
    #         p, t = self.query_stock_real_price()
    #         print ('>>(): stock price {}'.format(t, p))
    #         real_peice = float(p)
    #         self.q.put(real_peice)
    #         time.sleep(3)
    
    def stop_run(self):
        self._terminal = False

print(tushare.__version__)


#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./BLlib')
import tushare as ts
import BLFileUti,BLDate
import datetime,time,pandas

FILE_NAME = 'all_gupiao_code.txt'
FILE_NAME_Need = 'Need.txt'

# data = ts.get_hist_data('002596',start='2018-07-21')
# data = ts.get_hist_data('002596',start='2018-07-21') #获取周k线数据

# data = ts.get_hist_data('002596') #一次性获取全部日k线数据

# openM = data['ma5']

# temp_num = 0
# for num in openM:
#     temp_num += num

# ma5_avg = temp_num*1.0 / len(openM)
# print ma5_avg
# print data['open'] #['high'],['close'],['low'],['ma5'],['ma10']

def getAllCodeAndSaveToFile(fileName):
    '''
    fileName:保存文件的名称
    '''
    # 一次性获取最近一个日交易日所有股票的交易数据
    data = ts.get_today_all()
    # 获取所有股票代码
    data_code = data['code']
    dataTemp = []
    # 去除开头为3的股票代码(因为开头为3的，我还不能买，没用的数据)
    for t in data_code:
        if str(t).startswith('3'):
            continue
        else:
            dataTemp.append(t)
    # print dataTemp
    # 保存数据
    BLFileUti.writeArrDataToFile(fileName,dataTemp,way='w')

# 分析5日均线回升股
def analysis_ma5_rise(recentlyDayNum=5, mouthNum=1):
    '''
        recentlyDayNum: 最近几条数据-因为股市不包括周末，所以只拿最近的几条数据 （0，默认分析所有返回数据）
        mouthNum:最近几个月的数据,默认直接拿一个月数据
    '''
    allCode = BLFileUti.readFileGetArrData(FILE_NAME)
    startTime = BLDate.get_today_month(-mouthNum)

    needChooseArr = []

    for codeNum in allCode:
        # 获取个股历史交易记录
        df = ts.get_hist_data(code=codeNum,start=startTime)

        if df is None:
            print codeNum,"不需要关注"
            continue
        ma5Arr = df.ma5.values
        ma10Arr = df.ma10.values

        if len(ma5Arr) == 0 or len(ma10Arr) == 0:
            print codeNum,"不需要关注"
            continue

        if recentlyDayNum == 0:
            recentlyDayNum = len(ma5Arr)

        # 规则1：最近一个ma5 >= ma10(必须) 否则直接不关注
        if ma5Arr[0] < ma10Arr[0]:
            print codeNum,"不需要关注"
            continue
        # 规则2： 其他四个要求 ma10 > ma5 (现在默认分析五条数据)
        boolN = True
        if len(ma5Arr) >= recentlyDayNum:
            for i in range(recentlyDayNum,0,-1):
                ma5 = ma5Arr[i]
                ma10 = ma10Arr[i]
                if ma5 != 0 and ma10 != 0:
                    if ma5 > ma10:
                        print codeNum,"不需要关注"
                        boolN = False
                        break
        if boolN:
            print codeNum,"需要关注"
            needChooseArr.append(codeNum)

        # break
    if len(needChooseArr) > 0:
        print "需要关注的股票已保存"
        BLFileUti.writeArrDataToFile(FILE_NAME_Need,needChooseArr)
    else :
        print "没有需要关注的股票"


analysis_ma5_rise()
# startTime = BLDate.get_today_month(-1)
# df = ts.get_hist_data('600146',start=startTime)

# if df is None:
#     print "不需要关注"
# # if any(df):
# #     print "不需要关注"
# print df
# getAllCodeAndSaveToFile('all_gupiao_code.txt')

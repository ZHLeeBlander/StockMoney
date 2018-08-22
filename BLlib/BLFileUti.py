#!/usr/bin/python
# -*- coding: utf-8 -*-

def writeToFile(fileName, txt, way='a'):
    with open(fileName, way) as f:
        print(f.write(txt))

def writeArrDataToFile(fileName, arrData, way='a'):
    # 打开一个文件
    fo = open(fileName, way)
    for txt in arrData:
        fo.write(txt)
        fo.write('\n')
    # 关闭打开的文件
    fo.close()

def readFileGetArrData(fileName,way='r'):
    with open(fileName, way) as f:
        arrTemp =[]
        for line in f.readlines():
            arrTemp.append(line.strip())
        return arrTemp
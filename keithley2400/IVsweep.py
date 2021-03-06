#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import visa
import math
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

# 默认GPIB_address 地址为17（Keithley 2410）,2400为15
GPIB_address = 15
Default_filepath = 'B:/TestData/' + time.strftime("%Y%m%d", time.localtime()) + '/'


def open_file():
    filePath = input("输入文件路径：（'B:/TestData/160314/',可按回车跳过）")
    fileName = input('输入文件名称：(170KVg3V.txt)')
    if filePath == '':
        filePath = Default_filepath
    if filePath[-1] != '/':
        filePath += '/'
    if fileName[-4:] != '.txt':
        fileName += '.txt'
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    f = open(filePath + fileName, 'w')
    return f


def connect_inst():
    rm = visa.ResourceManager()
    inst = rm.open_resource('GPIB0::%d::INSTR' % GPIB_address)
    inst.write(':outp on')
    return inst


def close_inst(inst):
    inst.write("*RST")
    inst.write("*CLS")
    inst.write("SYSTEM:TIME:RESET:AUTO 0")
    inst.write(':outp off')


def IV_sweep(savefile, start=-3, end=3, step=60, delay=100, interval=300):
    """
    :param savefile: 测量数据保存文件地址
    :param GPIB_address: 测量仪器GPIB地址
    :param start: 起始测量电压
    :param end: 结束测量电压
    :param step: 测量分多少步进行
    :param delay: 测量延迟（ms）
    :param interval: 测量间隔（ms）
    :return:
    """
    inst = connect_inst()
    savefile.write('Voltage(V)'+'    '+'current(A)'+'    '+'    '+'time(s)'+'    '+'delay(ms)'+'    '
            +'interval(ms)'+'\n')

    Range = 1.1*(math.fabs(end) if math.fabs(end) > math.fabs(start) else math.fabs(start))
    inst.write(':SOUR:VOLT:RANG ' + str(Range))
    inst.write(':SOUR:DEL '+str(delay/1000))
    stage = (end - start)/step
    start_time = time.clock()
    # 开启实时绘图
    plt.ion()
    global Ilist
    Ilist = list()
    global Vlist
    Vlist = list()
    for i in range(step+1):
        V = start + stage*i
        inst.write(':source:volt %s' % V)
        inst.write('read?')
        #data = inst.read(':CURR')
        data = inst.read("TRACE:DATA")
        I = float(data.split(',')[1])
        t = time.clock() - start_time
        t = round(t, 2)
        V = round(V, 3)
        print(I, V, t)
        Ilist.append(I)
        Vlist.append(V)
        inst.write(':source:volt 0')
        time.sleep(interval/1000)
        plt.axis([min(Vlist)*1.1, max(Vlist)*1.1, min(Ilist), max(Ilist)])
        plt.plot(Vlist, Ilist, r'b-D')
        plt.pause(0.1)
        savefile.write(str(V)+'    '+str(I)+'           '+str(t)+'        '+str(delay)+'        '
                       + str(interval)+'\n')
        if i == step:
            savefig(savefile.name[:-4]+'.png')
            plt.ioff()
            plt.close()
            savefile.close()
    close_inst(inst)


if __name__ == '__main__':
    savefile = open_file()
    IV_sweep(savefile, start=-3, end=3, step=30, delay=100, interval=300)
    # 展示最后结果图像
    plt.axis([min(Vlist)*1.1, max(Vlist)*1.1, min(Ilist), max(Ilist)])
    plt.xlabel('voltage')
    plt.ylabel('current')
    plt.plot(Vlist, Ilist, 'r-o')
    plt.show()




#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import time
from TermControl import term_ctrl, current_term
from IVsweep import connect_inst, close_inst, open_file
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig


def R_T_curve(V, interval, startT, endT, speedT):
    """
    测量电阻随温度的变化，测量电压恒定
    :param V: 测量电阻时所加电压 V
    :param interval: 测量温度间隔 K
    :param startT: 起始温度 K
    :param endT: 目标温度   K
    :param speedT: 变温速率 K/min
    :return:
    """
    savefile = open_file()
    savefile.write('Voltage(V)    Current(A)+        Termperature(K)\n')
    term_ctrl(startT, endT, speedT)
    current_T = current_term()
    inst = connect_inst()
    plt.ion()
    Ilist = list()
    Tlist = list()
    inst.write(':SOUR:DEL '+str(0.1))
    while abs(current_T - endT) > 1:
        inst.write(':source:volt %s' % V)
        inst.write('read?')
        data = inst.read("TRACE:DATA")
        inst.write(':source:volt 0')
        I = float(data.split(',')[1])
        Ilist.append(I)
        Tlist.append(current_T)
        plt.xlim(min(Tlist)*1.1, max(Tlist)*1.1)
        plt.ylim( min(Ilist), max(Ilist))
        plt.plot(Tlist, Ilist, r'b-D')
        plt.pause(0.1)
        savefile.write(str(V)+'    '+str(I)+'        ' + str(current_T)+'\n')
        time.sleep(interval/speedT*60)
        current_T = current_term()
    close_inst(inst)
    savefile.close()
    plt.ioff()
    plt.close()
    plt.plot(Tlist, Ilist, r'b-D')
    plt.show()


if __name__ == '__main__':
    R_T_curve(2, 5, 220, 170, 0.5)

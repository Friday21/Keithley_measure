#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import visa
import time

# Model 331 GPIB_address=12
GPIB_address = 12


def connect_inst():
    rm = visa.ResourceManager()
    inst = rm.open_resource('GPIB0::%d::INSTR' % GPIB_address)
    return inst


def term_ctrl(start, end, speed):
    """
    :param start: 起始温度  K
    :param end: 目标温度    K
    :param speed: 变温速度  K/min
    :return:
    """
    inst = connect_inst()
    inst.write('ramp 1,0')
    time.sleep(0.5)
    inst.write('setp 1,' + str(start))
    time.sleep(0.5)
    inst.write('ramp 1,1,' + str(speed))
    time.sleep(0.5)
    inst.write('setp 1,' + str(end))


def current_term():
    """
    查询当前温度
    :return: current temperature
    """
    inst = connect_inst()
    term = float(inst.query('krdg? b'))
    print(term)
    return term

if __name__ == '__main__':
    term_ctrl(297, 240, 1)



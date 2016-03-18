#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from IVsweep import IV_sweep, open_file
from TermControl import current_term, term_ctrl


def IV_sweep_with_term_ctrl(savefile, startT, endT, speedT, startV, endV, stepV):
    term_ctrl(startT, endT, speedT)
    t = abs(endT - startT)/speedT*60
    time.sleep(t)
    current_T = current_term()
    while abs(current_T - endT) > 3:
        time.sleep(60)
        current_T = current_term()
    time.sleep(60*5)
    if abs(current_T - endT) < 3:
        IV_sweep(savefile, startV, endV, stepV, delay=100, interval=300)

if __name__ == '__main__':
    savefile = open_file()
    IV_sweep_with_term_ctrl(savefile, 240, 220, 0.3, -3, 3, 120)

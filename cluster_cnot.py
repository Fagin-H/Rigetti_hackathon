# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 20:51:20 2018

@author: fagin
"""

import pyquil.quil as pq
from pyquil.quil import Program
from pyquil import api
from pyquil.gates import *

qvm = api.QVMConnection()

def xmes(qu,cl):
    return [H(qu),MEASURE(qu,cl)]
    
def ymes(qu,cl):
    return [Z(qu),S(qu),H(qu),MEASURE(qu,cl)]

def zmes(qu,cl):
    return [MEASURE(qu,cl)]

def parcheck(inc,outc):
    tempp = Program().if_then(outc,Program(NOT(outc)))
    for i in inc:
        tempp.if_then(i,Program(NOT(outc)))
    return tempp

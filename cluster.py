# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyquil.quil as pq
from pyquil import api
from pyquil.gates import *

qvm = api.QVMConnection()

def xmes(qu,cl):
    return [H(qu),MEASURE(qu,cl)]
    
def ymes(qu,cl):
    return [Z(qu),S(qu),H(qu),MEASURE(qu,cl)]

def zmes(qu,cl):
    return [MEASURE(qu,cl)]

p = pq.Program([H(1),H(2),H(3),H(4),CZ(0,1),CZ(1,2),CZ(2,3),CZ(3,4)],zmes(0,[0]),ymes(1,[1]),ymes(2,[2]),ymes(3,[3]),H(4),zmes(4,[4]))

p2 = pq.Program(MEASURE(0,[0]))

qvm.run(p2,[0])
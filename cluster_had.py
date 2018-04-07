# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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


p = Program([X(0),H(1),H(2),H(3),H(4),
             zmes(0,[0]),
             CZ(0,1),CZ(1,2),CZ(2,3),CZ(3,4)],
                zmes(0,[0]),ymes(1,[1]),ymes(2,[2]),ymes(3,[3]),
                parcheck([0,2,3],5),
                parcheck([1,2],6),
                Program().if_then(6,Program(Z(4))),
                Program().if_then(5,Program(X(4))))

print(qvm.wavefunction(p))
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

connectors = [(7,2),(2,8),(8,13),(13,19),(19,14),(14,9),(0,6),(6,1),(1,12),(12,17),(17,11),(11,16),(12,18),(18,13)]
connectors1 = [(0,6),(9,14),(19,14),(13,19),(8,13),(2,8),(13,18),(12,18),(12,17),(17,11),(11,16),(7,12)]
connectors2 = [(7,2),(1,6)]

xmeasures = [0,7,2,8,19,14]
ymeasures = [6,1,12,17,11,18,13]

p = Program([H(i) for i in range(20) if i != 3 and i != 0 and i != 7 and i != 4 and i != 5 and i != 10 and i != 15],
            zmes(0,25),
            zmes(7,26),
            [CZ(i[0],i[1]) for i in connectors],
#            SWAP(7,1),
#            [CZ(i[0],i[1]) for i in connectors2],
            
            [xmes(i,i) for i in xmeasures],
            [ymes(i,i) for i in ymeasures],

            parcheck([1,6,17,11],20),
            parcheck([6,1,18,2,13,14],21),
            parcheck([0,1,12,17,18,7,8],22),
            parcheck([7,8,19],23),
            
            Program().if_then(20,X(16)),
            Program().if_then(21,X(9)),
            Program().if_then(22,Program(),Z(16)),
            Program().if_then(23,Z(9)),
            
            zmes(16,27),
            zmes(9,28)
        )


#print(qvm.wavefunction(p))
print(qvm.run(p,[25,26,27,28],5))
#data = qvm.run(p,[27],100)
#total = 0
#for i in data:
#    total += i[0]
#print(total)












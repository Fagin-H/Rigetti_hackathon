# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 20:51:20 2018

@author: fagin
"""

import pyquil.quil as pq
from pyquil.quil import Program
from pyquil import api
from pyquil.gates import *

from pyquil.api import CompilerConnection, get_devices
from pyquil.quil import Pragma

#devices = get_devices(as_dict=True)
#acorn = devices['19Q-Acorn']
#compiler = CompilerConnection(acorn)

qvm = api.QVMConnection()
qpu = api.QPUConnection('19Q-Acorn')

def xmes(qu,cl):
    return [H(qu),MEASURE(qu,cl)]
    
def ymes(qu,cl):
    return [Z(qu),S(qu),H(qu),MEASURE(qu,cl)]

def zmes(qu,cl):
    return [MEASURE(qu,cl)]


connectors = [(7,2),(2,8),(8,13),(13,19),(19,14),(14,9),(0,6),(6,1),(1,12),(12,17),(17,11),(11,16),(12,18),(18,13)]
connectors1 = [(0,6),(9,14),(19,14),(13,19),(8,13),(2,8),(13,18),(12,18),(12,17),(17,11),(11,16),(7,12)]
connectors2 = [(7,2),(1,6)]

xmeasures = [0,7,2,8,19,14]
ymeasures = [6,1,12,17,11,18,13]

p = Program([H(i) for i in range(20) if i != 3 and i != 0 and i != 4 and i != 5 and i != 10 and i != 15],
            [CZ(i[0],i[1]) for i in connectors1],
            SWAP(7,1),
            H(7),
            [CZ(i[0],i[1]) for i in connectors2],
            
            [xmes(i,i) for i in xmeasures],
            [ymes(i,i) for i in ymeasures],

            
            MEASURE(16,27),
            MEASURE(9,28),
            
        )

#job_id = compiler.compile_async(p)
#job = compiler.wait_for_job(job_id)
#
#print('compiled quil', job.compiled_quil())
#print('gate volume', job.gate_volume())
#print('gate depth', job.gate_depth())
#print('topological swaps', job.topological_swaps())
#print('program fidelity', job.program_fidelity())
#print('multiqubit gate depth', job.multiqubit_gate_depth())
data = qvm.run(p,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,25,26,27,28],100)
print(data)
#
#for item in data:
#    print(item[-4:])

#realdata = []
#for item in data:
#    if (item[1]+item[6]+item[17]+item[11]
#        ) % 2 == 0 and (item[6]+item[1]+item[18]+item[2]+item[13]+item[14]
#        ) % 2 == 0 and (item[0]+item[1]+item[12]+item[17]+item[18]+item[7]+item[8]
#        ) % 2 == 1 and (item[7]+item[8]+item[19]
#        ) % 2 == 0:
#        realdata.append(item[-4:])
#
#succhance = 0
#
#for item in realdata:
#    if item[0] == 0:
#        if item[2] == 0 and item[1] == item[3]:
#            succhance += 1
#    else:
#        if item[2] == 1 and item[1] != item[3]:
#            succhance += 1
#    
#succhance =  succhance*100/len(realdata)
#    
#print(str(succhance)+'% success, random chance = 25%')
#print(realdata)
    
    
    
    
    
    
    











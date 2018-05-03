# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyquil.quil as pq
from pyquil.quil import Program
from pyquil import api
from pyquil.gates import *
from pyquil.api import CompilerConnection, get_devices
from pyquil.quil import Pragma

devices = get_devices(as_dict=True)
acorn = devices['19Q-Acorn']
compiler = CompilerConnection(acorn)

qvm = api.QVMConnection()
qpu = api.QPUConnection('19Q-Acorn')


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

def postselect(data):
    newdata = []
    for item in data:
        if (item[0] + item[2] + item[3]) % 2 == 0 and (item[1] + item[2]) % 2 == 0:
            newdata.append([item[-1]])
    return newdata

p = Program([H(0),H(1),H(2),H(5),H(4)],
             [CZ(0,1),CZ(1,2),CZ(2,5),CZ(5,4)],
            H(0),Z(1),S(1),H(1),Z(2),S(2),H(2),Z(5),S(5),H(5),
            MEASURE(0,[0]),MEASURE(1,[1]),MEASURE(2,[2]),MEASURE(5,[3]),MEASURE(4,[4]))
#                xmes(0,[0]),ymes(1,[1]),ymes(2,[2]),ymes(3,[3]),zmes(4,[4]))
#                parcheck([0,2,3],5),
#                parcheck([1,2],6),
#                Program().if_then(6,Program(Z(4))),
#                Program().if_then(5,Program(X(4))))

#print(p)
#job_id = compiler.compile_async(p)
#job = compiler.wait_for_job(job_id)
#
#print('compiled quil', job.compiled_quil())
#print('gate volume', job.gate_volume())
#print('gate depth', job.gate_depth())
#print('topological swaps', job.topological_swaps())
#print('program fidelity', job.program_fidelity())
#print('multiqubit gate depth', job.multiqubit_gate_depth())

data = postselect(qpu.run(p,[0,1,2,3,4],10000))
amm = 0
for item in data:
    amm += item[0]
    
print(str(100*(1-amm/len(data)))+'% success, random chance = 50%')


















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
import numpy as np

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

def postselect(data):
    newdata = []
    for item in data:
        if (item[0] + item[2] + item[3]) % 2 == 0 and (item[1] + item[2]) % 2 == 0:
            newdata.append([item[-1]])
    return newdata

def prog(ini,fin):
    p = Program([ini,H(1),H(2),H(5),H(4)],
                [CZ(0,1),CZ(1,2),CZ(2,5),CZ(5,4)],
                H(0),Z(1),S(1),H(1),Z(2),S(2),H(2),Z(5),S(5),H(5),
                [MEASURE(0,[0]),MEASURE(1,[1]),MEASURE(2,[2]),MEASURE(5,[3]),fin])
    return p


def generate_data(trials):
    ins = [[I(0)],[X(0)],[H(0)],[Z(0),S(0),H(0)]]
    fins = [[MEASURE(4,[4])],[H(4),MEASURE(4,[4])],[Z(4),S(4),H(4),MEASURE(4,[4])]]

    for i in range(len(ins)):
        for j in range(len(fins)):
            p = prog(ins[i],fins[j])
            tempdata = qvm.run(p,[0,1,2,3,4],trials)
            np.save(open('haddata/data'+str(i)+str(j)+'.txt','wb'),tempdata)
    
def postselect_data():
    for i in range(4):
        for j in range(3):
            temp = np.load('haddata/data'+str(i)+str(j)+'.txt')
            temp = postselect(temp)
            np.save(open('posthaddata/postdata'+str(i)+str(j)+'.txt','wb'),temp)

#data = qvm.run(p,[0,1,2,3,4],10)
#np.save(open('data/test.txt','wb'),data)




















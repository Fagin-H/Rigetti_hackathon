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
from qutip import *
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

def postselect_had(data):
    newdata = []
    for item in data:
        if (item[0] + item[2] + item[3]) % 2 == 0 and (item[1] + item[2]) % 2 == 0:
            newdata.append([item[-1]])
    return newdata

def Hadamard(ini,fin):
    p = Program([ini,H(16),H(11),H(17),H(12)],
                [CZ(10,16),CZ(16,11),CZ(11,17),CZ(17,12)],
                H(10),Z(16),S(16),H(16),Z(11),S(11),H(11),Z(17),S(17),H(17),
                [MEASURE(10,[0]),MEASURE(16,[1]),MEASURE(11,[2]),MEASURE(17,[3]),fin])
    return p

def generate_had_data(trials):
    ins = [[I(10)],[X(10)],[H(10)],[H(10),S(10)]]
    fins = [[MEASURE(12,[4])],[H(12),MEASURE(12,[4])],[Z(12),S(12),H(12),MEASURE(12,[4])]]

    for i in range(len(ins)):
        for j in range(len(fins)):
            p = Hadamard(ins[i],fins[j])
            tempdata = qvm.run(p,[0,1,2,3,4],trials)
            np.save(open('haddata/data'+str(i)+str(j)+'.txt','wb'),tempdata)
    
def postselect_had_data():
    for i in range(4):
        for j in range(3):
            temp = np.load('haddata/data'+str(i)+str(j)+'.txt')
            temp = postselect_had(temp)
            np.save(open('posthaddata/postdata'+str(i)+str(j)+'.txt','wb'),temp)
            
def pi_over_2(ini,fin):
    p = Program([ini,H(16),H(11),H(17),H(12)],
                [CZ(10,16),CZ(16,11),CZ(11,17),CZ(17,12)],
                H(10),H(16),Z(11),S(11),H(11),H(17),
                [MEASURE(10,[0]),MEASURE(16,[1]),MEASURE(11,[2]),MEASURE(17,[3]),fin])
    return p

def generate_pi2_data(trials):
    ins = [[I(10)],[X(10)],[H(10)],[H(10),S(10)]]
    fins = [[MEASURE(12,[4])],[H(12),MEASURE(12,[4])],[Z(12),S(12),H(12),MEASURE(12,[4])]]

    for i in range(len(ins)):
        for j in range(len(fins)):
            p = pi_over_2(ins[i],fins[j])
            tempdata = qvm.run(p,[0,1,2,3,4],trials)
            np.save(open('pi2data/data'+str(i)+str(j)+'.txt','wb'),tempdata)
            
def postselect_pi2(data):
    newdata = []
    for item in data:
        if (item[0] + item[1] + item[2] + 1) % 2 == 0 and (item[1] + item[3]) % 2 == 0:
            newdata.append([item[-1]])
    return newdata
            
def postselect_pi2_data():
    for i in range(4):
        for j in range(3):
            temp = np.load('pi2data/data'+str(i)+str(j)+'.txt')
            temp = postselect_pi2(temp)
            np.save(open('postpi2data/postdata'+str(i)+str(j)+'.txt','wb'),temp)
            
def state_tomog(folder,inputt):
    expects = []
    for i in range(3):
        data = np.load(folder + '/postdata' + str(inputt) + str(i) + '.txt')
        expect = 1-2*np.mean(data)
        expects.append(expect)
    rho = 0.5*(qeye(2) + expects[0]*sigmaz() + expects[1]*sigmax() + expects[2]*sigmay())
    return rho
        
def process_tomog(folder):
    results = []
    for j in range(4):
        results.append(state_tomog(folder,j))
    rho00 = results[0]
    rho11 = results[1]
    rho01 = results[2] + 1j*results[3] - 0.5*(1+1j)*(results[0] + results[1])
    rho10 = results[2] - 1j*results[3] - 0.5*(1-1j)*(results[0] + results[1])
    rho_bar = Qobj(np.vstack((np.hstack((rho00.full(),rho01.full())),
                         np.hstack((rho10.full(),rho11.full())))))
    Lambda = 0.5*Qobj([[1,0,0,1],
                       [0,1,1,0],
                       [0,1,-1,0],
                       [1,0,0,-1]])
    chi = Lambda*rho_bar*Lambda
    return chi,qpt_plot_combined(chi,[["i", "x", "iy", "z"]],'Hadamard')
    

#data = qvm.run(p,[0,1,2,3,4],10)
#np.save(open('data/test.txt','wb'),data)




















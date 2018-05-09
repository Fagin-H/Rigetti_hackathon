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


qubits = [[10,16,11,17,12],[4,9,14,19,13]]


def postselect_had(data):
    newdata = []
    for item in data:
        if (item[0] + item[2] + item[3]) % 2 == 0 and (item[1] + item[2]) % 2 == 0:
            newdata.append([item[-1]])
    return newdata

def Hadamard(ini,fin,qubit):
    p = Program([ini,H(qubit[1]),H(qubit[2]),H(qubit[3]),H(qubit[4])],
                [CZ(qubit[0],qubit[1]),CZ(qubit[1],qubit[2]),CZ(qubit[2],qubit[3]),CZ(qubit[3],qubit[4])],
                H(qubit[0]),Z(qubit[1]),S(qubit[1]),H(qubit[1]),Z(qubit[2]),S(qubit[2]),H(qubit[2]),Z(qubit[3]),S(qubit[3]),H(qubit[3]),
                [MEASURE(qubit[0],[0]),MEASURE(qubit[1],[1]),MEASURE(qubit[2],[2]),MEASURE(qubit[3],[3]),fin])
    return p

def generate_had_data(trials,qubit):
    ins = [[I(qubit[0])],[X(qubit[0])],[H(qubit[0])],[H(qubit[0]),S(qubit[0])]]
    fins = [[MEASURE(qubit[4],[4])],[H(qubit[4]),MEASURE(qubit[4],[4])],[Z(qubit[4]),S(qubit[4]),H(qubit[4]),MEASURE(qubit[4],[4])]]

    for i in range(len(ins)):
        for j in range(len(fins)):
            p = Hadamard(ins[i],fins[j],qubit)
            tempdata = qvm.run(p,[0,1,2,3,4],trials)
            np.save(open('haddata/data'+str(i)+str(j)+'.txt','wb'),tempdata)
    
def postselect_had_data():
    for i in range(4):
        for j in range(3):
            temp = np.load('haddata/data'+str(i)+str(j)+'.txt')
            temp = postselect_had(temp)
            np.save(open('posthaddata/postdata'+str(i)+str(j)+'.txt','wb'),temp)
            
def pi_over_2(ini,fin,qubit):
    p = Program([ini,H(qubit[1]),H(qubit[2]),H(qubit[3]),H(qubit[4])],
                [CZ(qubit[0],qubit[1]),CZ(qubit[1],qubit[2]),CZ(qubit[2],qubit[3]),CZ(qubit[3],qubit[4])],
                H(qubit[0]),H(qubit[1]),Z(qubit[2]),S(qubit[2]),H(qubit[2]),H(qubit[3]),
                [MEASURE(qubit[0],[0]),MEASURE(qubit[1],[1]),MEASURE(qubit[2],[2]),MEASURE(qubit[3],[3]),fin])
    return p

def generate_pi2_data(trials,qubit):
    ins = [[I(qubit[0])],[X(qubit[0])],[H(qubit[0])],[H(qubit[0]),S(qubit[0])]]
    fins = [[MEASURE(qubit[4],[4])],[H(qubit[4]),MEASURE(qubit[4],[4])],[Z(qubit[4]),S(qubit[4]),H(qubit[4]),MEASURE(qubit[4],[4])]]

    for i in range(len(ins)):
        for j in range(len(fins)):
            p = pi_over_2(ins[i],fins[j],qubit)
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
    

def codeinfo():
    job_id = compiler.compile_async(Hadamard([I(10)],[MEASURE(12,[4])]))
    job = compiler.wait_for_job(job_id)
    
    print('compiled quil', job.compiled_quil())
    print('gate volume', job.gate_volume())
    print('gate depth', job.gate_depth())
    print('topological swaps', job.topological_swaps())
    print('program fidelity', job.program_fidelity())
    print('multiqubit gate depth', job.multiqubit_gate_depth())





















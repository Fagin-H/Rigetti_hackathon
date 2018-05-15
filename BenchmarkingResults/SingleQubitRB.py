# -*- coding: utf-8 -*-
from pyquil.quil import Program
from pyquil.api import QVMConnection
from random import choice
import numpy as np
from pyquil.gates import *
from math import pi
from pyquil.paulis import *
from pyquil.api import QVMConnection,QPUConnection, CompilerConnection
import pickle
import json


qvm = QVMConnection()
qpu = QPUConnection('19Q-Acorn')

from pyquil.api import get_devices
acorn = get_devices(as_dict=True)['19Q-Acorn']
qvmn = QVMConnection(acorn)

compiler = CompilerConnection(acorn)
devices = get_devices(as_dict=True)
acorn = devices['19Q-Acorn']
compiler = CompilerConnection(acorn)


comp_gates = {'RX(-pi/2) 0': 'RX(pi/2) 0',
              'RZ(-pi/2) 0': 'RZ(pi/2) 0',
              'RX(pi/2) 0': 'RX(-pi/2) 0',
              'RZ(pi/2) 0': 'RZ(-pi/2) 0'}
                       
paulis = {'RX(-pi) 0': 'RX(pi) 0',
          'RZ(-pi) 0': 'RZ(pi) 0',
          'RX(pi) 0': 'RX(-pi) 0',
          'RZ(pi) 0': 'RZ(-pi) 0'}

def benchmark_circuit(gates, max_length, interleaved = True):
    
    paulis = {'RX(-pi) 0': 'RX(pi) 0',
              'RZ(-pi) 0': 'RZ(pi) 0',
              'RX(pi) 0': 'RX(-pi) 0',
              'RZ(pi) 0': 'RZ(-pi) 0'}

    rand_circuit = []
    rand_inv_circuit = []
    for i in range(max_length):
            
        random_gate = choice(list(gates.keys()))
        inverse = gates[random_gate]
        rand_inv_circuit.append(inverse)
        rand_circuit.append(random_gate)
        
        random_pauli_gate = choice(list(paulis.keys()))
        inverse_pauli = paulis[random_pauli_gate]
        rand_inv_circuit.append(inverse_pauli)
        rand_circuit.append(random_pauli_gate)

    return (rand_inv_circuit, rand_circuit)
   
    
def create_quill_length(c,invc,l):
    
    p = Program().inst('PRAGMA PRESERVE_BLOCK')
    p.inst(c[0:2*l]) #remember this l and 4l for full circuit with inverses and interleaving
    p.inst('PRAGMA END_PRESERVE_BLOCK')
    p.inst(invc[0:2*l][::-1])
    p.measure(0,0)
    return p
          

def obtain_fidelities(gates,lengths,trials):    
    results = [] #indexed by k , as correct value always 0, summed up 1s/trials will give error prob for k
    stds = []
    c,inv = benchmark_circuit(gates,max(lengths)) 
   
    for l in lengths:
        rbc = create_quill_length(c,inv,l)
        job_id = compiler.compile_async(rbc)
        job = compiler.wait_for_job(job_id)

        print('compiled quil', job.compiled_quil())
        print('gate volume', job.gate_volume())
        print('program fidelity', job.program_fidelity())
        result = qvmn.run(rbc, [0], trials = trials)
        #print(rbc)
        #print(result)
        flat_list = [item for sublist in result for item in sublist]
        results.append(flat_list)
        stds.append(np.std(results))
    
    results = [sum(results[i])/trials for i in range(len(results))]  
    fidelities = [1-results[i] for i in range(len(results))]  
    
    return fidelities, stds
    
Ng = 3
lengths = range(1,100,2)
trials = 10000

final_results = [] #[j][k]_fi
stds = []

for j in range(Ng):
    F_j , std = obtain_fidelities(comp_gates,lengths,trials)
    final_results.append(F_j)
    stds.append(std)

    
averaged_fidelities = (1/Ng)*np.sum(np.array(final_results) , axis=0)  
std = np.mean(np.array(stds),axis=0) #switch to error propagation formula



with open("C:\\Users\\laura\\OneDrive\\Desktop\\Lab3\\NQVMTrials"+str(trials)+"Lengths"+str(max(lengths))+"Ng"+str(Ng)+".json", 'w') as fp:
    json.dump(final_results, fp)

with open("C:\\Users\\laura\\OneDrive\\Desktop\\Lab3\\NQVMTrialsSTDS"+str(trials)+"Lengths"+str(max(lengths))+"Ng"+str(Ng)+".json", 'w') as fp:
    json.dump(stds, fp)














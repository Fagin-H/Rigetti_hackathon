# -*- coding: utf-8 -*-
from pyquil.quil import Program
from pyquil.api import QVMConnection
from random import choice
import numpy as np
from pyquil.gates import *
from math import pi
from pyquil.paulis import *
from pyquil.api import QVMConnection
import pickle

qvm = QVMConnection()

comp_gates = {'RX(-pi/2) 0': 'RX(pi/2) 0',
                       'RY(-pi/2) 0': 'RY(pi/2) 0',
                       'RZ(-pi/2) 0': 'RZ(pi/2) 0',
                       'RX(pi/2) 0': 'RX(-pi/2) 0',
                       'RY(pi/2) 0': 'RY(-pi/2) 0',
                       'RZ(pi/2) 0': 'RZ(-pi/2) 0'}
                       
paulis = {'RX(-pi) 0': 'RX(pi) 0',
                       'RY(-pi) 0': 'RY(pi) 0',
                       'RZ(-pi) 0': 'RZ(pi) 0',
                       'RX(pi) 0': 'RX(-pi) 0',
                       'RY(pi) 0': 'RY(-pi) 0',
                       'RZ(pi) 0': 'RZ(-pi) 0'}

def benchmark_circuit(gates, max_length, interleaved = True):
    
    paulis = {'RX(-pi) 0': 'RX(pi) 0',
                       'RY(-pi) 0': 'RY(pi) 0',
                       'RZ(-pi) 0': 'RZ(pi) 0',
                       'RX(pi) 0': 'RX(-pi) 0',
                       'RY(pi) 0': 'RY(-pi) 0',
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
    
    p = Program().inst(c[0:2*l]) #remember this l and 4l for full circuit with inverses and interleaving
    p.inst(invc[0:2*l][::-1])
    p.measure(0,0)
    return p
          

def obtain_fidelities(gates,lengths,trials):    
    results = [] #indexed by k , as correct value always 0, summed up 1s/trials will give error prob for k

    c,inv = benchmark_circuit(gates,max(lengths)) 
   
    for l in lengths:
        rbc = create_quill_length(c,inv,l)
        #print(rbc)
        result = qvm.run(rbc, [0], trials = trials)
        flat_list = [item for sublist in result for item in sublist]
        results.append(flat_list)
        
    results = [sum(result[i])/trials for i in range(len(results))]  
    fidelities = [1-results[i] for i in range(len(results))]  
    
    return fidelities
    
Ng = 2
lengths = [2,4,6,8,10,12,14,16,18,20]
trials = 10 

final_results = [] #[j][k]

for j in range(Ng):
    F_j = obtain_fidelities(comp_gates,lengths,trials)
    final_results.append(F_j)

    
averaged_fidelities = (1/Ng)*np.sum(np.array(final_results) , axis=0)  
std = np.std(np.array(final_results),axis=0)

#eg= [0.1,0.2,0.2]
with open("C:\\Users\\laura\\OneDrive\\Desktop\\Lab3\\fidelity.txt", "wb") as fp:   #Pickling
    pickle.dump(final_results, fp)

with open("C:\\Users\\laura\\OneDrive\\Desktop\\Lab3\\fidelity.txt", "rb") as fp:   # Unpickling
    read_results = pickle.load(fp)
    
import matplotlib.pyplot as plt
#plt.scatter(4*np.array(lengths),averaged_fidelities)
plt.errorbar(np.array(lengths),averaged_fidelities,yerr=std, fmt='o')
plt.ylabel('Fidelity')
plt.xlabel('Circuit Length')
plt.show()


# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json

Ng = 3
lengths = 2*np.array(range(1,100,2)) #need this factor of two to compensate for an earlier mistake
trials = 10000



    
with open("C:\\Users\\laura\\OneDrive\\Desktop\\Lab3\\NQVMTrialsNoisyQVMTrials10000Lengths200Ng3.json", 'r') as fp:
    data = json.load(fp)
    

    
averaged_fidelities = (1/Ng)*np.sum(np.array(data) , axis=0)  
    
def func(m, A, B, f):
    return  A + B*f**m

popt, pcov = curve_fit(func, lengths,averaged_fidelities,p0=[0.6,0.5,0.97])

A=popt[0]
B=popt[1]
f=popt[2]


y = [func(x, A, B, f) for x in lengths]
plt.plot()
plt.plot(lengths,averaged_fidelities,'-b')
plt.plot(lengths, y, '-r')
plt.ylabel('Fidelity',fontsize='xx-large')
plt.xlabel('Circuit Length',fontsize='xx-large')
plt.title('Randomized Benchmarking: Noisy QVM',fontsize='xx-large')
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
text = '$f=0.994$'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(150, 0.87, text, fontsize=19,bbox=props)
plt.grid()
plt.show()

d = 2
Favg = ((d-1)*(1-f))/d

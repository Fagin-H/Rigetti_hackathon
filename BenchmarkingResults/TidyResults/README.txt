So the code implements the randomized benchmarking described in the first
few pages of the paper I've included. It's on z and x rotations by + and - pi/2 and + and - pi. 

In the file names I've included trials, Ng and lengths with the values following them. 
There's data with the and plots for the noisy qvm and the qpu for comparison.

Trials are the number of trials the QPU ran when calculating fidelities.

Ng refers to the number of different random gate sequences used. For Ng = 3 there are 
three different random gate sequences.

Lengths is just the max gate length the algorithm ran up to.

The data file is a list of three lists: data = [[gate_seq_1], [gate_seq_2], [gate_seq_3]] 
with gate_seq_1 = [f1, f2, ... fL], a list of average fidelities. i.e Ng = 3, lengths = L and
trials are number of calls to QPU when calculating f1,f2 etc.



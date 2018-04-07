# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyquil.quil as pq
from pyquil import api
from pyquil.gates import *

qvm = api.QVMConnection()

p = pq.Program(H(1),H(2),H(3),H(4),CZ(0,1),CZ(1,2),CZ(2,3),CZ(3,4),MEASURE(0,[0]))
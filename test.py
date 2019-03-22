# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 18:58:56 2017

@author: Gabriel
"""

import HEKAimport
import matplotlib.pyplot as plt

hf = HEKAimport.HEKAfile("test2.dat")

groupDict = hf.get_GroupDict()

print("All available groups:")
print(groupDict.keys())         

             
print("All series within E-28")
print("E-28")
for series in groupDict["E-28"].Series:
    print("---"+series.Label)
    #for sweep in series.Sweeps:
    #    print("|  |--"+sweep.Label)
        #for trace in sweep.Traces:
        #    print("|  |  L "+trace.Label)
   
plt.figure()
plt.plot(hf.get_Sweeps(groupDict["E-28"].Series[0]))
plt.show()


print(hf.get_IV(0.08, 3, 0))
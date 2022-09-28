# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 18:58:56 2017

@author: Gabriel
"""

from HEKAimport import HEKAimport
import matplotlib.pyplot as plt


hf = HEKAimport.HEKAfile()
hf.load_patchmaster("test2.dat")

print("All available groups:")
print(hf.keys())

             
"""print("All series within E-28")
print("E-28")
for series in hf["E-28"].Series:
    print("---"+series.Label)
    for sweep in series.Sweeps:
        print("|  |--"+sweep.Label)
        for trace in sweep.Traces:
            print("|  |  L "+trace.Label)


print("E-28\n\tL__IV")

for sweep in hf["E-28"].Series[0].Sweeps:
    for trace in sweep.Traces:
        print("\t\tL__", trace.Label)"""



df = hf["E-28"].Series[0].get_df()
df.plot(legend="False")
plt.show()

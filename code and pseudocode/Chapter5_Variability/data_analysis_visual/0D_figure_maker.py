# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:46:42 2016

@author: iar1g09
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt

import os
plt.rcParams.update(plt.rcParamsDefault)


path1 = 'results1D/both_check_start10000_pop_growth_on/worked/'
print path1
tested_values = [0.0001, 0.001, 0.01]
tested_As = [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95 ]
temp = []
columns = ["time", "V", "A", "sth"]


for v in tested_values:
    for a in tested_As:
        path = path1 + str(v) + '/' + "/A" + str(int(a*100)) + '/' 
        for file in os.listdir(path):
            current_file = os.path.join(path, file)

            df = pd.read_csv(current_file, names = columns, nrows = 1)
            df['V'] = v
            df['A'] = a
            temp.append(df)    
data1 = pd.concat(temp, ignore_index = True)   
data = data1.drop(["sth"], axis = 1)
data = data[data.time != 0]
data = data.convert_objects(convert_numeric=True)
data = data.dropna()

vs001 = data[data['V']==0.01]
vs0001 = data[data['V']==0.001]
vs00001 = data[data['V']==0.0001]
a_list = vs001.pivot_table('time', columns = 'A', aggfunc = 'mean')
b_list = vs0001.pivot_table('time', columns = 'A', aggfunc = 'mean')
c_list = vs00001.pivot_table('time', columns = 'A', aggfunc = 'mean')

fig, ax = plt.subplots(figsize = (4.92, 9.32))

plt.subplot(211)
plt.plot(a_list, 'o', markersize = 10, color = 'tomato', alpha = 0.8)
plt.subplot(211)
plt.plot(b_list, 's', color = 'cornflowerblue', markersize = 10,  alpha = 0.8)
plt.subplot(211)
plt.plot(c_list, '^', markersize = 10, color = 'forestgreen',  alpha = 0.8)

plt.gca().set_xlim([0.5, 1.0])
plt.gca().set_ylim([-0.0, 30000])

plt.gca().invert_xaxis()
plt.tick_params(labelbottom='off', labelleft = 'off', bottom = 'off', top = 'off', right = 'off', left = 'off')

#plt.axis('off')
#fig.set_size_inches(10, 10)
fig.savefig('both_check_start10k.png', transparent=True, bbox_inches = 'tight')
plt.show()


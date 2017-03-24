# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:46:42 2016

@author: iar1g09
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt

#plt.rcParams.update(plt.rcParamsDefault)
plt.style.use('ggplot')
start = ['0', '06', '12', '18', '25', '31', '37', '43']
keyword = ['Bar', 'NoBar']

#print path1
def make_file (key):
    path1 = '/Users/iar1g09/Dropbox/IZA/PHD/case_studies/variability_case_study/results2D/barrier/last_cell_' + str(key)    

    tested_seeds = [x + 1 for x in range(100)]
    tested_values = [0.001]
    tested_As = [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95 ]
    temp = []
    
    
    for seed in tested_seeds:
        for a in tested_As:
            for v in tested_values: 
                current_file = path1 + "/seed" + str(seed) + "/A" + str(int(a*100)) + '/' + 'barrier_' + str(v) + '.csv' 


                df = pd.read_csv(current_file,  skiprows = 1, header = None) # the row skipped is the time
                
                
                df['prop'] = df.mean(axis = 1)        # the mean value accross all time steps    
                df['V'] = v
                df['A'] = a
                  
                df['hot'] = df['prop'][0] - df['prop'][3]  # hot agents before - hot agents after
                df['cold'] = df['prop'][1] - df['prop'][4] # cold agents before - cold agents after
                df['ver'] = df['prop'][2] - df['prop'][5]  # vers agents before - vers agents after

                df = df[['V', 'A', 'hot', 'cold', 'ver']]

                temp.append(df.iloc[:1])   # all the six lines are identical now, we only need the first one
        
    data = pd.concat(temp, ignore_index = True) 
    print data.head(20)
    
    # prep for plotting
    a_list = data.pivot_table('hot', columns = 'A')
    b_list = data.pivot_table('cold', columns = 'A')
    c_list = data.pivot_table('ver', columns = 'A')
    print a_list, b_list, c_list
    
    
    # plot
    fig, ax = plt.subplots(figsize = (4.92, 9.32))
    #plt.figure()
   # plt.subplot(211)
    #plt.plot((a_list+b_list/2), color = 'tomato', alpha = 0.8,label = 'specialists')
    plt.subplot(211)
    plt.plot(a_list, color = 'tomato',  alpha = 0.8)
    plt.subplot(211)
    plt.plot(b_list, color = 'cornflowerblue', alpha = 0.8)
    plt.subplot(211)
    plt.plot(c_list,  color = 'forestgreen',  alpha = 0.8, label = 'versatilist')
    plt.xlim(0.60, 0.95)
    plt.legend(fontsize = 10)
    #fig.savefig('2D_all_sep_start'+ start +'.png', transparent=False, bbox_inches = 'tight')
    fig.savefig('around_barrier_all'+ key +'.png', transparent=False, bbox_inches = 'tight')
   
    plt.show()

for i in keyword:
    make_file(i)
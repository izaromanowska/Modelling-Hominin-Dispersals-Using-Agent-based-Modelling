# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 09:49:49 2016

@author: iar1g09
"""

from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import os
plt.style.use('ggplot')
path1 = 'results1D/both_data_k10/worked/'

tested_values = [0.001]#[0.0001, 0.001, 0.01]
tested_As = [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95 ]
temp = []



for v in tested_values:
    for a in tested_As:
        path = path1 + str(v) + "/A" + str(int(a*100)) + '/'
       # print path
        for file in os.listdir(path):
            if file == '.DS_Store': # skip over system files
                pass
            elif file.startswith("pop_size"): # skip over files with pop size
                pass
            else:
                current_file = os.path.join(path, file)                
                with open(current_file) as f:
                    first_line = f.readline()
                    ncols = len(f.readline().split(','))
                # skip the first row and the first column    
                df = pd.read_csv(current_file, skiprows = 1, usecols = range(1, ncols), header = None)                
                                
                
                df['V'] = v
                df['A'] = a  
                df['mean']= df.mean(axis=1)
                df['ID'] = [0,1,2,3,4,5]
                df = df[['ID', 'V', 'A','mean']]
                temp.append(df)
            
data = pd.concat(temp, ignore_index = True)  
print data.head() 
vs01 = data[data['V']==0.01]
vs001 = data[data['V']==0.001]
vs0001 = data[data['V']==0.0001]
  
a_list = vs01.pivot_table('mean', columns = ['A'], index =[ 'ID'], aggfunc = 'mean')
b_list = vs001.pivot_table('mean', columns = ['A'], index =[ 'ID'], aggfunc = 'mean')
c_list = vs0001.pivot_table('mean', columns = ['A'], index =[ 'ID'], aggfunc = 'mean') 

plt.figure(figsize=(30,40), dpi = 600)
#fig, ax = plt.subplots(sharex = True)
fitness_list = ["fitness boost 0.01", "fitness boost 0.001", "fitness boost 0.0001"]
lists = [b_list]#[a_list, b_list, c_list]


 #ABSOLUTE NUMBERS
for i in range(1): # we're making three plots for 0.01, 0.001 and 0.0001
    plt.subplot(3, 1, i+1)    
    
    plt.plot(lists[i].iloc[5]/lists[i].iloc[2], 'o', label='versatilist', color = 'forestgreen', markersize = 25) # plot the versatilist
    plt.plot(lists[i].iloc[5]/lists[i].iloc[2], '--', color = 'forestgreen', linewidth = 4) # plot the versatilist

    #plot both specialists as one
    #plt.plot(((lists[i].iloc[4]/lists[i].iloc[1])+(lists[i].iloc[3]/lists[i].iloc[0]))*0.5, 'o', label='specialists', color = "darkmagenta", markersize = 25)
    #plt.plot(((lists[i].iloc[4]/lists[i].iloc[1])+(lists[i].iloc[3]/lists[i].iloc[0]))*0.5, '--', color = "darkmagenta", linewidth = 4)

    #plot both specialists separately
    plt.plot(lists[i].iloc[4]/lists[i].iloc[1], 'o',label='cold', color = 'cornflowerblue', markersize = 25)
    plt.plot(lists[i].iloc[3]/lists[i].iloc[0],'o', label='hot', color = 'tomato', markersize = 25)
    plt.plot(lists[i].iloc[4]/lists[i].iloc[1], '--', color = 'cornflowerblue', linewidth = 4)
    plt.plot(lists[i].iloc[3]/lists[i].iloc[0], '--', color = 'tomato', linewidth = 4)
    
    #adjust the plot

    plt.legend(fontsize = 30)
    plt.xlim(0.60, 0.95)
    plt.ylabel("Proportion each gene: mig/pop", fontsize = 35)
    plt.tick_params(reset = True, labelsize=30)
    plt.xlabel("Environmental fluctuations (alpha)", fontsize = 35)
    plt.tight_layout()

    '''
    if i == 2:
        plt.tick_params(top ='off', labelsize=16)
        plt.xlabel("Environmental fluctuations (alpha)", fontsize = 20)
    else:
        plt.tick_params(labelbottom='off', top ='off', labelsize=16)
    '''    
"""  

# RELATIVE NUMBERS
for i in range(3): # we're making three plots for 0.01, 0.001 and 0.0001
    plt.subplot(3, 1, i+1)    
    
    plt.plot((lists[i].iloc[5] / (lists[i].iloc[2] + lists[i].iloc[5])),label='versatilist', linewidth = 3) # plot the versatilist
    #plot both specialists as one
    #plt.plot(((lists[i].iloc[4] / (lists[i].iloc[4] + lists[i].iloc[1]))+(lists[i].iloc[3] / (lists[i].iloc[3] + lists[i].iloc[0])))*0.5, label='specialists', linewidth = 3)
    
    #plot both specialists separately
    plt.plot((lists[i].iloc[4] / (lists[i].iloc[4] + lists[i].iloc[1])), label='cold', linewidth = 3)
    plt.plot((lists[i].iloc[3] / (lists[i].iloc[3] + lists[i].iloc[0])), label='hot', linewidth = 3)
    
    #adjust the plot
    plt.legend(fontsize = 16)
    plt.xlim(0.60, 0.95)
    plt.title(fitness[i], fontsize = 20)
    plt.ylabel("Proportion of each gene", fontsize = 20)
    if i == 2:
        plt.tick_params(top ='off', labelsize=16)
        plt.xlabel("Environmental fluctuations (alpha)", fontsize = 20)

    else:
        plt.tick_params(labelbottom='off', top ='off', labelsize=16)
"""        
plt.savefig("whosDispersing1_diff_MigByPop_spec_k10.png")
plt.show()

#vers_migr = a_list[a_list['ID']==5]    
#print vers_migr 
#plt.plot(vers_migr) 
'''
h_list = [(e_list[i]/(a_list[i] + e_list[i])) if a_list[i] else (a_list[i] + 0) for i in range(len(e_list))]
i_list = [(f_list[i]/(b_list[i] + f_list[i])) if b_list[i] else (b_list[i] + 0) for i in range(len(f_list))]
j_list = [(g_list[i]/(c_list[i] + g_list[i])) if c_list[i] else (c_list[i] + 0) for i in range(len(g_list))]
'''


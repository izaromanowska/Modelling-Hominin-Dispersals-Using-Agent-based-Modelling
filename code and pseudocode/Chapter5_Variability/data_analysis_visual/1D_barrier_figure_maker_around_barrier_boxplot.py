# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:46:42 2016

@author: iar1g09
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

#import os
#plt.rcParams.update(plt.rcParamsDefault)
plt.style.use('ggplot')
start = ['0', '06', '12', '18', '25', '31', '37', '43']
keyword = ['Bar']

#print path1
def make_file (key):
    path1 = '/Users/iar1g09/Dropbox/IZA/PHD/case_studies/variability_case_study/results2D/barrier/BigBar_Bar'     

    tested_seeds = [x + 1 for x in range(50)]
    tested_values = [0.001]
    tested_As = [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95 ]
    temp = []
    #columns = [ "time1", "time2", "V", "A", "ID", "diff_barrier", "diff_end", "timeOnBarrier", "timeOnEnd" ]
    
    
    for seed in tested_seeds:
        for a in tested_As:
            for v in tested_values: 
                current_file = path1 + "/seed" + str(seed) + "/A" + str(int(a*100)) + '/' + 'startPreBar_' + str(v) + '.csv' 

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

    boxColors = ['tomato', 'cornflowerblue', 'forestgreen']
 
    # plot
    fig, ax1 = plt.subplots(figsize = (4.92, 9.32))

    data1 = [ data[data['A']==0.60][['hot']],data[data['A']==0.60][['cold']], data[data['A']==0.60][['ver']],
              data[data['A']==0.65][['hot']],data[data['A']==0.65][['cold']], data[data['A']==0.65][['ver']],
              data[data['A']==0.70][['hot']],data[data['A']==0.70][['cold']], data[data['A']==0.70][['ver']],
              data[data['A']==0.75][['hot']],data[data['A']==0.75][['cold']], data[data['A']==0.75][['ver']],
              data[data['A']==0.80][['hot']],data[data['A']==0.80][['cold']], data[data['A']==0.80][['ver']],
              data[data['A']==0.85][['hot']],data[data['A']==0.85][['cold']], data[data['A']==0.85][['ver']],
              data[data['A']==0.90][['hot']],data[data['A']==0.90][['cold']], data[data['A']==0.90][['ver']],   
              data[data['A']==0.95][['hot']],data[data['A']==0.95][['cold']], data[data['A']==0.95][['ver']]]   
        
    bp = plt.boxplot(data1)

    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    numBoxes = 8*3
    medians = list(range(numBoxes))
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        boxCoords = list(zip(boxX, boxY))
        # Alternate between colours
        k = i % 3
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            plt.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
    names = ['A60','A65', 'A70','A75', 'A80','A85', 'A90', 'A95']        
    xtickNames = plt.setp(ax1, xticklabels=np.repeat(names, 3))
    plt.setp(xtickNames, rotation=45, fontsize=8)
    '''plt.subplot(211)
    plt.plot(a_list, color = 'tomato',  alpha = 0.8)
    plt.subplot(211)
    plt.plot(b_list, color = 'cornflowerblue', alpha = 0.8)
    plt.subplot(211)
    plt.plot(c_list,  color = 'forestgreen',  alpha = 0.8, label = 'versatilist')
    plt.xlim(0.60, 0.95)
    plt.legend(fontsize = 10)'''
    #fig.savefig('2D_all_sep_start'+ start +'.png', transparent=False, bbox_inches = 'tight')
    fig.savefig('1stPreBar_bigBar_all'+ key +'_boxplot.png', transparent=False, bbox_inches = 'tight')
   
    plt.show()

for i in keyword:
    make_file(i)
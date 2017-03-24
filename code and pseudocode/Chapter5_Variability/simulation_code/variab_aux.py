# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 15:50:11 2015

@author: iar1g09
"""
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import Counter



box_colors = ['#bd0026', '#f03b20', '#fd8d3c', '#fecc5c', '#ffffb2', '#ffffcc','#f1eef6', '#bdc9e1', '#74a9cf', '#2b8cbe', '#045a8d']

# <codecell>

def visualisation(world, time):
    """ A whole procedure to visualise the world. Not great but will do for now """
    
    # _________ init values _________
    array = np.array(world)                 # turn in to numpy
    x, y = array.shape                      # give it dimensions
    c = 1                                   # start the counter
    fig = plt.figure()                      # start the figure 

    fig.suptitle(('The world at time', time), fontsize=14, fontweight='bold')



    # __________ PROCEDURES __________

    for i in range (x):
        for j in range (y):

            # it chokes on empty lists so we fill them with a 0, it's not displayed and do not change anything in calculations
            if not array[i][j]:              
                array[i][j].append(0)

            ax = plt.subplot(x, y, c)        # the +1 is because the plotting was starting from 

            counts, bins, patches = ax.hist(array[i][j], bins = range(1,11), facecolor = 'yellow', edgecolor = 'gray') # a numpy command which takes the list and calculates frequencies for a histogram
            #ax.set_xticks(bins)
            #ax.set_ylim(0, len(array[i][j]))       # yes axis labels
            ax.set_xticks([])                       # no axis labels
            ax.set_yticks([])
            
            for patch, value in zip(patches, bins[:]):      # make each bar different colour
                patch.set_facecolor(box_colors[value])
            c+=1
    
    file_name = 'results'+str(time)+'.png'                  # save the plot to file, name = number of the time step visualised
    plt.subplots_adjust(wspace = 0.0, hspace = 0.0)         # put the grid squares closely touching
    
    plt.savefig(file_name, format = 'PNG')                 # You can save the figure to file... 
    #plt.show()                                              # and/or just show it on the screen (comment out one of the options).


# <codecell>

def element_count(p):
    """Auxilary function to count the total number of agents in all squares - only for testing"""
    elements = list(p)
    count = 0
    while elements:
        entry = elements.pop()
        count += 1
        if isinstance(entry, list):
            elements.extend(entry)
    return count


# <codecell>

def freq_count(world):

    numbers = Counter(world)

    values = []
    for i in range(1, 7):
        a = numbers.get(i)
        a = int(0 if a is None else a) # turning None values - happens if there are no agents of a given type - into 0
        values.append(a)


    Gene1 = values[0] * 2 + values[1] + values[2] # hot
    Gene2 = values[5] * 2 + values[2] + values[4] # cold
    Gene3 = values[3] * 2 + values[1] + values[4] # variab

    Total = Gene1 + Gene2 + Gene3
    if Total == 0:
        Total = 1

    return Gene1/Total, Gene2/Total, Gene3/Total


# <codecell>

def write_data(time, a_list, b_list, c_list, V, e_list = [], f_list = [], g_list = [], PATH = 'results1D'):
    """ Writing the output into a csv file """
    
    # TO CREATE CSV FILE
    with open(PATH + str(V) + '.csv', 'ab') as f:
        writer = csv.writer(f)                          # use the csv writer
        writer.writerow([time, 0])        
        writer.writerow(a_list)                        # write data
        writer.writerow(b_list)
        writer.writerow(c_list)
        writer.writerow(e_list)                        # write data
        writer.writerow(f_list)
        writer.writerow(g_list)
        f.close()                                       # close file


# <codecell>

def write_people(people, V, path, PATH):
    """ Writing the output into a csv file """
    p = PATH + str(V) + '_' + str(path) +'.csv'
    #print p
    # TO CREATE CSV FILE
    with open(p, 'ab') as f:
        writer = csv.writer(f)                          # use the csv writer
        writer.writerow(people)                        # write data

        f.close()                                       # close file



# <codecell>

def population_counter(world1, a_list, b_list, c_list, V, PATH):
    a, b, c = freq_count(world1)
    a_list.append(a)
    b_list.append(b)
    c_list.append(c)
    path = 'population'
    write_people(world1, V, path, PATH)


# <codecell>

def migrant_counter(migrants, e_list, f_list, g_list, V, PATH):
    e, f, g = freq_count(migrants)
    e_list.append(e)
    f_list.append(f)
    g_list.append(g)
    path = 'migrants'
    write_people(migrants, V, path, PATH)


# <codecell>

def make_plot(a_list, b_list, c_list, V, PATH, path1):
    plt.figure(figsize = (16, 7), dpi = 300)
    plt.subplot(211)
    plt.plot(a_list , color = 'r')
    plt.subplot(211)
    plt.plot(b_list , color = 'b')
    plt.subplot(211)
    plt.plot(c_list , color = 'g')
    file_name = str(PATH) + str(path1)+ str(V) + '.png'                  # save the plot to file, name = number of the time step visualised
    plt.savefig(file_name, format = 'PNG', dpi = 300)
    plt.clf()

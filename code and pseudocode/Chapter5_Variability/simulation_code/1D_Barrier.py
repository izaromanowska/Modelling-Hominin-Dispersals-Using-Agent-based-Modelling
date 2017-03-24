# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 16:19:48 2016

@author: iar1g09
"""

# <nbformat>3.0</nbformat>
# -*- coding: utf-8 -*-



# <codecell>

from __future__ import division
from sys import exit
import math, random
from variab_aux1 import *
from histogram_test_final1 import visual3D
import numpy as np


# <codecell>

# ____________________  GLOBAL VARIABLES _______________________

# world dimensions
X_MAX = 21
Y_MAX = 3


# number of simulated iterations
MAX_TIME = 2000

# how often do you want to see the visualisation
VISUAL = 5

# seting the multiplicant for the probability of migration - keep between 0-1
MIG_CONST = 0.1

# how many steps for the sin cycle
T = 50

# the growth rate of the population
GROWTH = 0.20 # this growth rate of 20% is equivalent to 1% per anum (given 1 generation = 20 years)   
#GROWTH = 0.02 # this growth rate of 2% is equivalent to 0.1% per anum (given 1 generation = 20 years)

# Steepness of the migration curve
K = 5 

# choose the algorithm for deciding which cell is the best: 1 = random; 2 = least occupied cell; 3 = highest fitness; 4 = go only in one direction (right)
MIGRATION_TYPE = 4

# Define alpha
#A = 0.95

#if A > 1 or A < 0.5:
#	exit ("alpha needs to be larger than 0.5 smaller than 1") # this will stop the execution of the script
# In the original study the model was formulated for 0.5 < alpha < 1 hence all the problems with negative numbers

# Define carrying capacity
# the global_cc will have to changes from a set value to a friction map in 2D scenarios
CC = 1000                      # the cc of the cell - this should come from a friction map, it's static at the moment
CC2 = CC * 0.1
hot = [1,] * 100               # proportion of the population hot, cold and vers
cold = [6,]* 100
vers = [4,]* 100


STARTING_POP = hot + cold + vers
# global for testing (at the end of the main)
#travellers = 0

# <codecell>

def write_values(PATH, seed, A, V):
    output = open(PATH + 'seed' + str(seed)+ '/A'+ str(int(A*100))  + '/details.txt', 'w')
    output.write('no of iterations {time};\n full sin cycle every {sin} steps; \n output every {st} steps; \n starting population {sp}; \n proportion cold specialist {p1}; \n proportion hot specialist {p2}; \n proportion versatilits {p3}; \n alpha {a}; \n carrying capacity in normal cells {cc1};\n carrying capacity in special cells {cc2}; \nmigration multiplier {mig}; \n migration type {migtype}; \n seed {seed1};'.format(time = str(MAX_TIME), sin = str(T), st = str(VISUAL), sp = str(len(STARTING_POP)), p1 = str(len(hot)/len(STARTING_POP)),  p2 = str(len(cold)/len(STARTING_POP)),  p3 = str(len(vers)/len(STARTING_POP)), a = str(A), cc1 = str(CC), cc2 = str(CC2), mig = str(MIG_CONST), migtype = str(MIGRATION_TYPE), seed1 = str(seed))) # write the basics
    output.close()


# <codecell>
# Combination matrix used in the "reproduction" procedure

# ____________replication  matrix_________________

comb_matrix = np.array([
[(1, ),        (1, 2),         (1, 3),         (2, ),      (2, 3),         (3, )],
[(1, 2),       (1, 2, 2, 4),   (1, 2, 3, 5),   (2, 4),     (2, 3, 4, 5),   (3, 5)],
[(1, 3),       (1, 2, 3, 5),   (1, 3, 3, 6),   (2, 5),     (2, 3, 5, 6),   (3, 6)],
[(2, ),        (2, 4),         (2, 5),         (4, ),      (4, 5),         (5, )],
[(2, 3),       (2, 3, 4, 5),   (2, 3, 5, 6),   (4, 5),     (4, 5, 5, 6),   (5, 6)],
[(3, ),        (3, 5),         (3, 6),         (5, ),      (5, 6),         (6, )]  ])



def fitness(temp, V, A):
    """ # Fitness function is used to calculate the current fitness of a given genotype.
    It applies the equations below and returns a list of fitness values for the current temperature.
    """
# Define gamma (alpha + gamma = 1)
    G = 1 - A
# updated fitness scores
    w11 = A + G * temp                              # fit[0]
    w12 = (2 * A + G * temp + V) * 0.5              # fit[1]
    w13 =  A                                        # fit[2]
    w22 = A + V                                     # fit[3] (added)
    w23 = (2 * A - G * temp + V) * 0.5              # fit[4]
    w33 = A - G * temp                              # fit[5]

    fitness = [w11, w12, w13, w22, w23, w33]                       # crt a list of fitnesses
    if all(i >= 0 and i <= 1 for i in fitness): # this lines just checks that all values are between 0 - 1, if they're not it will kick the fuss
      return fitness
    else:
      print ('sth seriously wrong with the fitness values, exceeded the range')
      print V
      print temp
      print fitness


# <codecell>
def nok(agents, cc):
    """This function determines the number of children for the next generation from the logistic growth function"""
   
   # _________ init values _________
    no_of_people = len(agents)                   # determine number of agents on the cell
 
    # __________ PROCEDURES __________
    if no_of_people >= 2:                        # if there is a minimum of 2 people on the cell:
        new_no_of_kids = no_of_people + GROWTH * no_of_people * ((cc - no_of_people)/cc) # plug in the population growth curve
        if new_no_of_kids >= cc:                  # if the number of children is too high, curb them down to cc
            return int(round(cc))
        else:
            kids = int(round(new_no_of_kids)) 
            return kids        # return the number of people in the next generation (rounded to the nearest integer)
        
        assert kids <= cc

    else:
        return 0                              # if there's 0 or 1 agent left return 0


# <codecell>


def reproduction (agents, no_of_kids, current_fitnesses):
    """produces a list of agents in the cell for the next step
# The reproduction procedure consists of the following steps:
# • determining the fitness of every agent in the cell
# • determining the number of descendants (the nok function calculates that on the basis of the total fitness and carrying capacity)
# • roulette wheel function produces 2 parents
# • one of the possible combination of the parents' genes is chosen at random - the child is born
# • the child is appended to the list that will be returned to the main function"""

    # _________ init values _________
    children = []	

    # __________ PROCEDURES __________
    
    cumul = set_up_roulette(agents, current_fitnesses)    
    
    # Determine the agents in the cell in the next step
    for i in range(no_of_kids):
        mum, dad = roulette(cumul)        # use the roulette wheel to draw two parents from the pool of all agents
        kid = random.choice(comb_matrix[mum-1, dad-1])    # choose at random from one of the possible combinations of their genes (-1 is used for the same reason as 2 notes above)
        children.append(kid)                              # append to the list of kids which will be returned
    return children


# <codecell>

def set_up_roulette(agents, current_fitnesses):
    """ Auxilary function setting up a roulette wheel.
        Significant gains in terms of time and comp power. 
    """
# _________ init values _________
    agents_local = list(agents)       # make a local copy             
    counts = []
    cumul = []
   
    for agent_type in range(1, 7):                          
        counts.append(agents_local.count(agent_type))               # count how many agents of each type there are
        cumul.append(counts[agent_type-1] * current_fitnesses[agent_type-1]) # multiply the no of agents of each type by their fitness (e.g. 5 agents of type 1, each with fitness 0.5 = 2.5)
    cum_sum = np.cumsum(cumul) # create a cumulative sum of the fitness of each type, i.e. 1 = 2.5, 2 = 5.6, 3 = 4.1 then [2.5, 8.1, 12.2]

    assert len(cum_sum) == 6
    
    return(list(cum_sum))
    
# <codecell>

def roulette(cumul):
    """ Auxilary function running a roulette wheel on a list of agents. 
    The roulette wheel chooses two agents with a probability weighted on each agent's fitness
    """
    parents = []

    for i in range(2):                          # do the following twice:

        hit = random.uniform(0.0, cumul[5])        # draw a random number between 0 and the total fitness of all agents
            
        for agent_type in xrange(6):               # as you go through the list of fitness values...
            if cumul[agent_type] >= hit:           # ... and if the sum is higher that the random number... 
                
                parents.append(agent_type + 1)     # append the agent to the list of parents (agents 1-6, index 0-5 hence +1)
                break                              # had to break the loop because otherwise all agents after the one chosen will be added (they're all 'now > hit')
    
    # sanity checks
    for i in parents: 
        assert i >=1 and i <=6
    assert len(parents) == 2
    
    return parents


# <codecell>

def migration(agents, current_fitnesses, cell_up, cell_down, cell_left, cell_right, m_fitness, current_cc):
    """ Migration procedure, agents have a given chance (determined by their fitness + local population size) to move to one of the 4 neighbouring cells """

# _________ init values _________

    spread_cells = [cell_up, cell_down, cell_left, cell_right]
    updated_cells = [[],[],[],[]]
    cell_here = []
    migrants = []
    group_size = len(agents)  

    
    
    for x in range (group_size):    # each child is considered separately

    # _________ init values _________
        traveller = agents.pop()                # consider (and remove) the first kid from the list 
        migrate = random.uniform(0.0, 1)        # draw a random number
        cell_fitness = []
       
    # __________ PROCEDURES __________
    
        # calculate individual fitness in respect to mean fitness of the group
        x = (current_fitnesses[traveller - 1] - m_fitness) / m_fitness 
        
        # calculate individual probability of migrating
        prob_of_migra = (group_size / current_cc) * (1 / (1 + math.e**(K * x)))

        # must be between 0 and 1
        assert prob_of_migra <= 1 and prob_of_migra >= 0, "group: {group}, prob: {prob1}, fst part: {fp}, snd part: {sp}, group size: {gs}, cc1: {cc1}, k: {K1}, m_fitness: {m_fitness1}, agent: {agent}".format(group = str(group_size), prob1 = str(prob_of_migra), fp = str((group_size / current_cc)), sp = str(1 / (1 + math.e**(K * x))), gs = str(len(agents)), cc1 = str(current_cc), K1 = str(K), m_fitness1 = str(m_fitness), agent = str(current_fitnesses[traveller - 1]))  

        # migrate with a previously calculated probability 
        if migrate <= MIG_CONST * prob_of_migra:     # if the random number is lower that the calculated probability of migration (mig_const = 1 -> standard migration rate)
            migrants.append(traveller) 
             
            if MIGRATION_TYPE == 1:   #  choose a cell at random
                best_cell = random.randint(0, 3)

            elif MIGRATION_TYPE == 2: # least occupied cell
                cell_fitness = [(1 - ((len(cell) + 1) / cc)) for cell in spread_cells]
                best_cell = random.choice([i for i, j in enumerate(cell_fitness) if j == max(cell_fitness)]) 
           
            elif MIGRATION_TYPE == 3:                      # mixed
                cell_fitness = [current_fitnesses[traveller - 1] * (1 - ((len(cell) + 1) / cc)) for cell in spread_cells]
                best_cell = random.choice([i for i, j in enumerate(cell_fitness) if j == max(cell_fitness)])    
            
            else: 
                best_cell = 3   # migration only to the right
       
            updated_cells[best_cell].append(traveller)           # add the kid to the list of that cell

        else:
            cell_here.append(traveller)                          # if they didn't migrate append them to the list for cell here
    updated_cells.append(cell_here)
    updated_cells.append(migrants)
   
    return updated_cells




# <codecell>


 
def process(world_now, temp, V, A):
    """Draws the current list of agents and returns a new one for the next step
    A wrap up function to call all steps of the process from one place. 
    Runs the simulation on each cell of the grid.
    """
    
   # _________ init values _________
    world_next = [[[] for x in xrange(X_MAX)] for x in xrange(Y_MAX)]
    world_final = [[[] for x in xrange(X_MAX)] for x in xrange(Y_MAX)] 
    migrants = []
    current_fitnesses = fitness(temp, V, A) # get the current fitness level for each type of an agent
 
   
        
        
#==============================================================================
# ___________________ MIGRATION  ___________________ 
#==============================================================================
    for cellY in range (1, Y_MAX - 1):                 # loop through the world 
       
       for cellX in range (1, X_MAX - 1):                       
            
            # get the list of agents on this cell
            agents = world_now[cellY] [cellX]               
            
            if agents:
                # setup the barrier                
                if cellX == (X_MAX - 1) * 0.5:          
                    current_cc = CC2    
                elif cellX == ((X_MAX - 1) * 0.5) - 1:          
                    current_cc = CC2
                elif cellX == ((X_MAX - 1) * 0.5) + 1:          
                    current_cc = CC2
                else:
                    current_cc = CC 
                
                # get the current values of the cells around this cell
                cell_up = world_now[cellY - 1][cellX] [:]        
                cell_down = world_now[cellY + 1][cellX] [:]
                cell_left = world_now[cellY][cellX - 1] [:]
                cell_right = world_now[cellY][cellX + 1] [:]
    
                # calculate the fitness of each agent                         
                agents_fitnesses = [current_fitnesses[agent - 1 ] for agent in agents]     # create a list of their fitnesses (note that agents are 1,2,3... while indexing goes 0, 1, 2...)
                # calculate the average fitness                
                m_fitness = reduce(lambda x, y: x + y, agents_fitnesses) / len(agents_fitnesses)
    
                # __________________ Migration procedure ___________________  
                add_cell_up, add_cell_down, add_cell_left, add_cell_right, add_cell_here, migrants = migration(agents[:], current_fitnesses, cell_up, cell_down, cell_left, cell_right, m_fitness, current_cc)
                   
                # ___________________ Update the cells _____________________          
    
                world_next[cellY - 1] [cellX][:] = world_next[cellY - 1] [cellX][:] + add_cell_up[:]        # update the cells around 
                world_next[cellY + 1] [cellX][:] = world_next[cellY + 1] [cellX][:] + add_cell_down[:]       
                world_next[cellY] [cellX - 1][:] = world_next[cellY] [cellX - 1][:] + add_cell_left[:]
                world_next[cellY] [cellX + 1][:] = world_next[cellY] [cellX + 1][:] + add_cell_right[:]
                  
                world_next[cellY][cellX][:] = world_next[cellY][cellX][:] + add_cell_here[:]                # update the cell here

    
#==============================================================================
#     # _______________ REPRODUCTION_______________
#==============================================================================
    
    for cellY in range (1, Y_MAX - 1):                            # loop through the world
        for cellX in range (1, X_MAX - 1):                        # python can take -1 while looping - it is the last element of the list i.e. the empty boundary actually works for N and E because it refers to the cells on the other side (the S and w boundary)
            agents = world_next[cellY] [cellX]   
            if agents:
                if cellX == (X_MAX - 1) * 0.5:          
                    current_cc = CC2    
                elif cellX == ((X_MAX - 1) * 0.5) - 1:          
                    current_cc = CC2
                elif cellX == ((X_MAX - 1) * 0.5) + 1:          
                    current_cc = CC2
                else:
                    current_cc = CC
    
            # ___________________ Reproduction procedure ____________________
                 
                #when MIGRATION OFF change to:
                #agents = world_now[cellY] [cellX]                                       # get the list of agents on this cell
                if len(agents) > 0:
    
                  # Determine how many agents the cell will hold in the next step
                  no_of_kids = nok(agents, current_cc)

                  # reproduction procedure based on roulette
                  children = reproduction(agents, no_of_kids, current_fitnesses)              # determine the children
                 
                  # Upload the new generation into the right cell
                  world_final[cellY][cellX][:] = children
                  assert len(children) <= no_of_kids, "people_here: {children}, no_thats_supposed_to_be_here: {nok}".format(children(str(len(children))), nok = str(no_of_kids))
    
    return world_final, migrants # COMMENT IN FOR EXPERIMENTS WITH MIGRATION


# <codecell>

def main (A, V, path, seed):
    """ Main loop"""

    # _________ init values _________
    random.seed(seed)                     # uses seed for reproducibility
    time_counter = random.randint(1,50)   # initialise time from a random point (0 - hot start, 25 - cold start)
    start_time = time_counter
    write_values(path, seed, A, V)        # create a file with the setup details of the simulation

    been = 0        # only record time once
    times = [start_time]  # record what the start time was
    times_end = [start_time]
    a_list = []
    b_list = []
    c_list = []
    
    e_list = []
    f_list = []
    g_list = []
    
    h_list = []
    i_list = []
    j_list = []    

    k_list = []
    l_list = []
    m_list = []      
    
    # Create the grid
    cells = []
    world = [[ cells for x in xrange(X_MAX)] for x in xrange(Y_MAX)] 
    
    # Initialise the population on the leftmost cell
    world [1][1] = STARTING_POP             

    while time_counter < MAX_TIME:
        # calculate the current temprerature
        temp = math.sin( (time_counter / T) * 2 * math.pi)           
        
        # run the main simulation loop
        world, migrants = process(world, temp, V, A)            # this is the main function, shit happens exactly here
        
        # visualisation procedure every so many loop iterations 
  #      if time_counter % VISUAL == 0:          # spit out the results

          # visualisation(world, time_counter)
          #  population_counter(world[1][1], a_list, b_list, c_list, V, PATH)
          #  migrant_counter(migrants, e_list, f_list, g_list, V, PATH) # this pops up an error 'Error: total = 0' because the function that calculates it (freq_count) doesn't expect to be getting noone 
          #  pop_list.append(element_count(world))
     #       visual3D(np.array(world), time_counter - start_time, A, V, seed, X_MAX, Y_MAX, Path = 'results2D/barrier/hot_scenario/pics/')
        
#==============================================================================
#          Data collection
#==============================================================================
        # Data collection when agents cross the barrier        
        barrier_cell = int((X_MAX - 1) * 0.5)    # middle cell
        
        if world[1][barrier_cell + 2]:# and been == 0: # if the barrier is crossed we record data (only once)
            if been == 0:
                times.append(time_counter - start_time)               # record time at the barrier
                been = 1                                 # a block to prevent recording time at every step 
            if time_counter % VISUAL == 0:          # spit out the results
                a, b, c = freq_count(world[1][barrier_cell - 2]) # agents proportions before the barrier
                a_list.append(a)
                b_list.append(b)
                c_list.append(c)
                
                e, f, g = freq_count(world[1][barrier_cell + 2]) # agents proportions after the barrier
                e_list.append(e)
                f_list.append(f)
                g_list.append(g)
                
                k, l, m = freq_count(world[1][1]) # agents proportions on the first cell
                k_list.append(k)
                l_list.append(l)
                m_list.append(m)
        
        # Data collection when agents reach the end of the world          
        if world[1][X_MAX-2]:
            #h, i, j = freq_count(world[1][X_MAX-2]) # agents proportions 
            break    
#==============================================================================
#             if been == 1:
#                 times_end.append(time_counter - start_time)               # record time at the end
#                 been = 2                                 # a block to prevent recording time at every step 
#==============================================================================
                
#==============================================================================
#             if been == 2:
#                 if time_counter % VISUAL == 0:          # spit out the results  
#                     h_list.append(h)
#                     i_list.append(i)
#                     j_list.append(j)
#                 
#                 if h == 0.0 and i == 0.0 :
#                     times_end.append(time_counter - start_time)
#                     write_data(times_end, k_list, l_list, m_list, V, h_list, i_list, j_list, PATH="results2D/barrier/last_cell_Bar/" +"worked/" + str(V) + "/A" + str(int(A*100)) + "/" + str(seed))
#                     break
#                 # stop the simulation          
#                 if j == 0.0:
#                     times_end.append(time_counter - start_time)
#                     break
#==============================================================================
#            
            # write data to file
            
       # break
        time_counter += 1     # time changes by 1 step 
    #save
    # save pop pre barier + pop post barrier    
    write_data(times, a_list, b_list, c_list, V, e_list, f_list, g_list, PATH = path + "seed" + str(seed) + "/A" + str(int(A*100)) + "/barrier_")
    # save pop 1st cell + pop last cell     
    #write_data(times, k_list, l_list, m_list, V, h_list, i_list, j_list, PATH = path + "seed" + str(seed) + "/A" + str(int(A*100)) + "/startEnd_")
    # save pop 1st cell + pop post barrier
    write_data(times, k_list, l_list, m_list, V, e_list, f_list, g_list, PATH = path + "seed" + str(seed) + "/A" + str(int(A*100)) + "/startPostBar_")
    write_data(times, k_list, l_list, m_list, V, a_list, b_list, c_list, PATH = path + "seed" + str(seed) + "/A" + str(int(A*100)) + "/startPreBar_")

  

def testing ():
    tested_seeds = [x + 1 for x in range(100)]    
    tested_values = [ 0.0001, 0.001, 0.01 ]
    tested_As = [ 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    PATH = "results2D/barrier/"
    for seed in tested_seeds:    
        for a in tested_As:  
            for v in tested_values:
                main(a, v, PATH, seed)
    


testing()

# <codecell>



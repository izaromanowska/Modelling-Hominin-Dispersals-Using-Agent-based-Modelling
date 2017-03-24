# <nbformat>3.0</nbformat>
# -*- coding: utf-8 -*-



# <codecell>

from __future__ import division
from sys import exit
import math, random
from variab_aux import *
import numpy as np
import matplotlib.pyplot as plt 
#import matplotlib.ticker as ticker


# <codecell>

# ____________________  GLOBAL VARIABLES _______________________

# world dimensions
X_MAX = 3
Y_MAX = 3

SEED = 1

# number of simulated iterations
MAX_TIME = 100

# how often do you want to see the visualisation
VISUAL = 1000

# seting the multiplicant for the probability of migration - keep between 0-1
MIG_CONST = 0

# how many steps for the sin cycle
T = 50

# the growth rate of the population
GROWTH = 0.20 # this growth rate of 20% is equivalent to 1% per anum (given 1 generation = 20 years)   
#GROWTH = 0.02 # this growth rate of 2% is equivalent to 0.1% per anum (given 1 generation = 20 years)

# Steepness of the migration curve
K = 5 

# choose the algorithm for deciding which cell will be the destination: 
# 1 = random; 2 = density dep; 3 = a combination of indiv and group
MIGRATION_TYPE = 1

# Define alpha
A = 0.75
if A > 1 or A < 0.5:
	exit ("alpha needs to be larger than 0.5 smaller than 1") # this will stop the execution of the script
# In the original study the model was formulated for 0.5 < alpha < 1 

# Define gamma (alpha + gamma = 1)
G = 1 - A

# Define carrying capacity => will be later developed as a non-heterogenous and dynamic map of cc
# the global_cc will have to change from a generic number to a value in the friction map
cc = 10000                      

# initial proportion of the population hot, cold and vers
hot = [1,] * 4950               
cold = [6,]* 4950
vers = [4,]* 100

STARTING_POP = hot + cold + vers
# global for testing (at the end of the main)
#travellers = 0
# path used to save results
PATH = "results1D/replication/seed" + str(SEED) + "/A" + str(A*100)


# <codecell>
# Combination matrix used in the "reproduction" procedure


# ____________replication  matrix used in the roulette wheel _________________

comb_matrix = np.array([
[(1, ),        (1, 2),         (1, 3),         (2, ),      (2, 3),         (3, )],
[(1, 2),       (1, 2, 2, 4),   (1, 2, 3, 5),   (2, 4),     (2, 3, 4, 5),   (3, 5)],
[(1, 3),       (1, 2, 3, 5),   (1, 3, 3, 6),   (2, 5),     (2, 3, 5, 6),   (3, 6)],
[(2, ),        (2, 4),         (2, 5),         (4, ),      (4, 5),         (5, )],
[(2, 3),       (2, 3, 4, 5),   (2, 3, 5, 6),   (4, 5),     (4, 5, 5, 6),   (5, 6)],
[(3, ),        (3, 5),         (3, 6),         (5, ),      (5, 6),         (6, )]  ])


# <codecell>

def write_values():
    """Produces a file recording all parameter values of the run scenario and places it in the same folder."""
    output = open(PATH + 'details.txt', 'w')
    output.write('no of iterations {time};\n full sin cycle every {sin} steps; \n output every {st} steps; \n starting population {sp}; \n proportion cold specialist {p1}; \n proportion hot specialist {p2}; \n proportion versatilits {p3}; \n alpha {a}; \n migration multiplier {mig}; \n migration type {migtype}; \n seed {seed1};'.format(time = str(MAX_TIME), sin = str(T), st = str(VISUAL), sp = str(len(STARTING_POP)), p1 = str(len(hot)/len(STARTING_POP)),  p2 = str(len(cold)/len(STARTING_POP)),  p3 = str(len(vers)/len(STARTING_POP)), a = str(A), mig = str(MIG_CONST), migtype = str(MIGRATION_TYPE), seed1 = str(SEED))) # write the basics
    output.close()


# <codecell>

def fitness(temp, V):
    """ # Fitness function is used to calculate the current fitness of a given genotype.
    It applies the equations below and returns a list of fitness values for the current temperature.
    """

# updated fitness scores
    w11 = A + G * temp                              # fit[0]
    w12 = (2 * A + G * temp + V) * 0.5              # fit[1]
    w13 =  A                                        # fit[2]
    w22 = A + V                                     # fit[3] 
    w23 = (2 * A - G * temp + V) * 0.5              # fit[4]
    w33 = A - G * temp                              # fit[5]
    
    fitness = [w11, w12, w13, w22, w23, w33]            #  crt a list of fitnesses
    if all(i >= 0 and i <= 1 for i in fitness):         #  checks that all values are between 0 - 1
      return fitness
    else:
      print ('sth seriously wrong with the fitness values, exceeded the range')
      print V
      print temp
      print fitness


# <codecell>
def nok(agents):
    """This function determines the number of children for the next generation from the logistic growth function"""
   
   # _________ init values _________
    no_of_people = len(agents)                   # determine number of agents on the cell
 
    # __________ PROCEDURES __________
    if no_of_people >= 2:                        # if there is a minimum of 2 people on the cell:
        new_no_of_kids = no_of_people + GROWTH * no_of_people * ((cc - no_of_people)/cc) # plug in the population growth curve
        return int(round(new_no_of_kids))#, cc    # return the number of people in the next generation (rounded to the nearest integer)
   
    #    return len(STARTING_POP), cc            # FOR REPLICATION OF GROVE2010 ONLY - there was no population size change in the orginal study
    else:
        return 0                                 # if there's 0 or 1 agent left return 0


# <codecell>


def reproduction (agents, no_of_kids, current_fitnesses):
    """produces a list of agents in the cell for the next step
    # The reproduction procedure consists of the following steps:
# • determining the fitness of every agent in the cell
# • determining the number of descendants (the nok function calculates that on the basis of the carrying capacity)
# • roulette wheel function produces 2 parents
# • one of the possible combination of the parents' genes is chosen at random - the child is born
# • the child is appended to the list that will be returned to the main function"""

    # _________ init values _________
    children = []	

    # __________ PROCEDURES __________
    
    # auxilary function for setting up the roulette wheel    
    cumul = set_up_roulette(agents, current_fitnesses)    
    
    # Determine the agents in the cell in the next step
    for i in range(no_of_kids):
        mum, dad = roulette(cumul)        # use the roulette wheel to draw two parents from the pool of all agents
        kid = random.choice(comb_matrix[mum-1, dad-1])    # choose at random from one of the possible combinations of their genes (-1 is used because indexing starts ay 0)
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
  
  # _________ init values _________    
        hit =  random.uniform(0.0, cumul[5])        # draw a random number
    # __________ PROCEDURES __________
            
        for agent_type in xrange(6):    # as you go through the list of fitness values...
    
        if cumul[agent_type] >= hit:                            # ... and if the sum is higher that the random number... 
                
                parents.append(agent_type + 1)      # append the agent to the list of parents (agents 1-6, index 0-5 hence +1)
                break                               # had to break the loop because otherwise all agents after the one chosen will be added (they're all 'now > hit')
    for i in parents: 
        assert i >=1 and i <=6
    assert len(parents) == 2
    return parents


# <codecell>

def migration(agents, current_fitnesses, cell_up, cell_down, cell_left, cell_right, m_fitness):
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
        prob_of_migra = MIG_CONST * (group_size / cc) * (1 / (1 + math.e**(K * x)))
        assert prob_of_migra <= 1 and prob_of_migra >= 0 # must be between 0 and 1

        # migrate with a previously calculated probability 
        if migrate <= prob_of_migra:     # if the random number is lower that the calculated probability of migration (mig_const = 1 -> standard migration rate)
            migrants.append(traveller) 
            
            if MIGRATION_TYPE == 1:   #  choose a cell at random - it does not matter in zero dimentional scenarios
              best_cell = random.randint(0, 3)

            elif MIGRATION_TYPE == 2: # group
              cell_fitness = [(1 - ((len(cell) + 1) / cc)) for cell in spread_cells]
              best_cell = random.choice([i for i, j in enumerate(cell_fitness) if j == max(cell_fitness)])  # gives an index of the best cell, if there are more cells with the same value then one is chosen at random
         
            else:                      # mixed
              cell_fitness = [current_fitnesses[traveller - 1] * (1 - ((len(cell) + 1) / cc)) for cell in spread_cells]
              best_cell = random.choice([i for i, j in enumerate(cell_fitness) if j == max(cell_fitness)])    
        
            updated_cells[best_cell].append(traveller)           # add the kid to the list of that cell

        else:
            cell_here.append(traveller)                          # if they didn't migrate append them to the list for cell here
   
    updated_cells.append(cell_here)
    updated_cells.append(migrants) # this is auxilary for recording the composition of the migrants
   
    return updated_cells



def process(world_now, temp, V):
    """Draws the current list of agents and returns a new one for the next step
    A wrap up function to call all steps of the process from one place. 
    Runs the simulation on each cell of the grid.
    """
    
   # _________ init values _________
    world_next = [[[] for x in xrange(X_MAX)] for x in xrange(Y_MAX)]
    world_final = [[[] for x in xrange(X_MAX)] for x in xrange(Y_MAX)] 
 
    current_fitnesses = fitness(temp, V)        # get the current fitness level for each type of an agent
   
  
# FROM HERE COMMENTED OUT for experiments without migration
    for cellY in range (1, Y_MAX - 1):                            # loop through the world 
        for cellX in range (1, X_MAX - 1):                        # python can take -1 while looping - it is the last element of the list i.e. the empty boundary actually works for N and E because it refers to the cells on the other side (the S and w boundary)

# ___________________ Migration procedure ___________________

            # _________ init values _________

            cell_up = world_now[cellY - 1][cellX] [:]        # get the current values of the cells around this cell
            cell_down = world_now[cellY + 1][cellX] [:]
            cell_left = world_now[cellY][cellX - 1] [:]
            cell_right = world_now[cellY][cellX + 1] [:]

            agents = world_now[cellY] [cellX]               # get the list of agents on this cell
            agents_fitnesses = [current_fitnesses[agent - 1 ] for agent in agents]     # create a list of their fitnesses (note that agents are 1,2,3... while indexing goes 0, 1, 2...)
           
            m_fitness = reduce(lambda x, y: x + y, agents_fitnesses) / len(agents_fitnesses)

            if len(agents) > 0: 
              add_cell_up, add_cell_down, add_cell_left, add_cell_right, add_cell_here, migrants = migration(agents[:], current_fitnesses, cell_up, cell_down, cell_left, cell_right, m_fitness)
               
         # ___________________ Update the cells ___________________           

              world_next[cellY - 1] [cellX][:] = world_next[cellY - 1] [cellX][:] + add_cell_up[:]        # update the cells around 
              world_next[cellY + 1] [cellX][:] = world_next[cellY + 1] [cellX][:] + add_cell_down[:]       
              world_next[cellY] [cellX - 1][:] = world_next[cellY] [cellX - 1][:] + add_cell_left[:]
              world_next[cellY] [cellX + 1][:] = world_next[cellY] [cellX + 1][:] + add_cell_right[:]
              world_next[cellX][cellY][:] = world_next[cellX][cellY][:] + add_cell_here[:]                # update the cell here

    # everyone who needed to migrate migrated, people have babies now
    #UNTIL HERE COMMENTED OUT for experiments without migration 

    for cellY in range (1, Y_MAX - 1):                            # loop through the world
        for cellX in range (1, X_MAX - 1):                        # python can take -1 while looping - it is the last element of the list i.e. the empty boundary actually works for N and E because it refers to the cells on the other side (the S and w boundary)


        # ___________________ Reproduction procedure ____________________
             
            agents = world_next[cellY] [cellX]   
            #when MIGRATION OFF change to:
            #agents = world_now[cellY] [cellX]                                       # get the list of agents on this cell
            if len(agents) > 0:
              
              # Determine how many agents the cell will hold in the next step
              no_of_kids = nok(agents)
              
              # reproduction procedure based on roulette
              children = reproduction(agents, no_of_kids, current_fitnesses)              # determine the children
             
              # reproduction procedure based on tournament
              #children = tournament(agents, no_of_kids, current_fitnesses, sum=sum)

              # Upload the new generation into the right cell
              world_final[cellY][cellX][:] = children

    return world_final, migrants # COMMENT OUT 'migrants'  FOR EXPERIMENTS WITH MIGRATION


# <codecell>

def main (V):
    """ Main loop, many of the output precedures can be found in the variab_aux library"""

    # _________ init values _________
    random.seed(SEED)                              # uses seed for reproducibility
    time_counter = 0                             # initialise time
    write_values()
    migrants_total = []

  #  temp_counter = 0                             # initialise temperature curve
    a_list = [0.495,]
    b_list = [0.495,]
    c_list = [0.10,]
    
    e_list = [0.495,]
    f_list = [0.495,]
    g_list = [0.10,]
    
    pop_list = []
    # Create the grid
    cells = []
    world = [[ cells for x in xrange(X_MAX)] for x in xrange(Y_MAX)] # xrange is just a quicker version of range in iterables 
    world [1][1] = STARTING_POP

    while time_counter < MAX_TIME:
    
        temp = math.sin( (time_counter / T) * 2 * math.pi)           # temp is a sin wave for now
       # CHANGE FOR EXPERIMENTS WITHOUT MIGRATION
       # world = process(world, temp, V) 
        
        world, migrants = process(world, temp, V)            # this is the main function, shit happens exactly here
        
        # visualisation procedure every so many loop iterations 
        if time_counter % VISUAL == 0:          # spit out the results

            visualisation(world, time_counter)
            population_counter(world[1][1], a_list, b_list, c_list, V, PATH)
      #      migrant_counter(migrants, e_list, f_list, g_list, V, PATH) # this may pop up an error 'Error: total = 0' because the function that calculates it (freq_count) doesn't expect to be getting noone 
            pop_list.append(element_count(world))

        # if any one of the genes died you can just as well finish the run, so that it doesn't churn pointless numbers
        a, b, c = freq_count(world[1][1]) 
       
        if a == 0.0 and b == 0.0 or c == 0.0:
            print
            print str(time_counter)
            print "the process was broken cos someone died out"
            print (element_count(world))
            print a, b, c
            break
        time_counter += 1     # time changes by 1 step 


    make_plot(a_list, b_list, c_list, V, PATH, path1 = "population")

    plt.plot(pop_list)
    plt.savefig(PATH + str(V) + 'population_count' + '.png', format = 'PNG', dpi = 300)
    write_data(a_list, b_list, c_list, V, PATH) #e_list, f_list, g_list, V)
       
#       decomment for calculating the total number of agents in all of the cells
#       total_pop = element_count(world) 
#       print total_pop - (X_MAX * Y_MAX + X_MAX) # it counts all elements of the array, including the lists themselves so the total agent number = total number - number of lists in the matrix

def testing ():
    tested_values = [0.0001, 0.001, 0.01]

    for i in tested_values:
        main(i)


testing()

# <codecell>



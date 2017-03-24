from __future__ import division
import csv, random
import numpy as np
import matplotlib.pyplot as plt

#import ipdb



# GLOBAL VARIABLES

# World dimensions
X_MAX = 265
Y_MAX = 435

# Number of simulated iterations
MAX_TIME =  2250 # 4500 #

# Number of groups on each starting cell
STARTING_POP = 	10

# Frequency of exporting the output 
STEP = 100 #250 #500 #

# How often the map changes
MAP_CHANGE = 10 # 20 #

# different scenarios: 0 - baseline; 1 - with diseases, 2 - divided by 100
SICK = 0

# Enviro values for runs
# 1: polar; 2: boreal; 3: cold temperate; 4: warm temperate; 5: subtropical; 6: tropical; 7: equatorial; 8: desert; 9: water/ice 
# Pop Growth: Pal; CC: Plant Mobile Average
if SICK == 1:
	print "sick"
# this set of runs curbs down the pop growth in equatorial and tropical conditions
	run1 = {1: [1.01005, 0.10, 3.625], 	2: [1.01005, 0.20, 5.5], 	3: [1.03043, 0.30, 4.75], 		4:[1.03043, 0.40, 9.5], 	5:[1.03043, 0.60, 13.5], 	6:[1.005025, 0.60, 27.125], 7: [1.005025, 0.40, 25.375], 8: [1.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Mobile Average
	run2 = {1: [2.717, 0.10, 3.625], 	2: [2.717, 0.20, 5.5], 		3: [7.374, 0.30, 4.75], 		4:[7.374, 0.40, 9.5], 		5:[7.374, 0.60, 13.5], 		6:[1.8585, 0.60, 27.125], 	7: [1.8585, 0.40, 25.375], 	8: [1.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Plant Mobile Maximum
	run3 = {1: [1.01005, 0.10, 8.375], 	2: [1.01005, 0.20, 11.0], 	3: [1.03043, 0.30, 23.75], 		4:[1.03043, 0.40, 20.75], 	5:[1.03043, 0.60, 33.0], 	6:[1.005025, 0.60, 53.75], 	7: [1.005025, 0.40, 41.5], 	8: [1.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Mobile Maximum
	run4 = {1: [2.717, 0.10, 8.375], 	2: [2.717, 0.20, 11.0], 	3: [7.374, 0.30, 23.75], 		4:[7.374, 0.40, 20.75], 	5:[7.374, 0.60, 33.0], 		6:[1.8585, 0.60, 53.75], 	7: [1.8585, 0.40, 41.5], 	8: [1.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Plant Stable Average
	run5 = {1: [1.01005, 0.10, 8.375], 	2: [1.01005, 0.20, 28.625], 3: [1.03043, 0.30, 125.375],	4:[1.03043, 0.40, 47.375], 	5:[1.03043, 0.60, 51.0], 	6:[1.005025, 0.60, 91.125], 7: [1.005025, 0.40, 63.5], 	8: [1.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Stable Average
	run6 = {1: [2.717, 0.10, 8.375], 	2: [2.717, 0.20, 28.625], 	3: [7.374, 0.30, 125.375], 		4:[7.374, 0.40, 47.375], 	5:[7.374, 0.60, 51.0], 		6:[1.8585, 0.60, 91.125], 	7: [1.8585, 0.40, 63.5], 	8: [1.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Animal Average
	run7 = {1: [1.01005, 0.10, 3.625], 	2: [1.01005, 0.20, 2.375],	3: [1.03043, 0.30, 6.625],		4:[1.03043, 0.40, 4.125], 	5:[1.03043, 0.60, 4.375], 	6:[1.005025, 0.60, 10.0], 	7: [1.005025, 0.40, 25.0], 	8: [1.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Animal Average
	run8 = {1: [2.717, 0.10, 3.625], 	2: [2.717, 0.20, 2.375], 	3: [7.374, 0.30, 6.625], 		4:[7.374, 0.40, 4.125], 	5:[7.374, 0.60, 4.375], 	6:[1.8585, 0.60, 10.0], 	7: [1.8585, 0.40, 25.0], 	8: [1.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Animal Max
	run9 = {1: [1.01005, 0.10, 8.375], 	2: [1.01005, 0.20, 4.375], 	3: [1.03043, 0.30, 12.0],		4:[1.03043, 0.40, 5.25], 	5:[1.03043, 0.60, 4.375], 	6:[1.005025, 0.60, 19.375], 7: [1.005025, 0.40, 41.5], 	8: [1.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Animal Maximum
	run10 = {1: [2.717, 0.10, 8.375], 	2: [2.717, 0.20, 4.375], 	3: [7.374, 0.30, 12.0], 		4:[7.374, 0.40, 5.25], 		5:[7.374, 0.60, 4.375], 	6:[1.8585, 0.60, 19.375], 	7: [1.8585, 0.40, 41.5], 	8: [1.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}

if SICK == 2:
	# This setup curbes down population growth by a factor of 100 - used to test extreme scenario
	# Pop Growth: Pal; CC: Plant Mobile Average
	run1 = {1: [0.0000001, 0.10, 3.625], 	2: [0.0000001, 0.20, 5.5], 	3: [0.0000003, 0.30, 4.75], 		4:[0.0000003, 0.40, 9.5], 	5:[0.0000003, 0.60, 13.5], 	6:[0.0000001, 0.60, 27.125], 	7: [0.0000001, 0.40, 25.375], 8: [0.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Mobile Average
	run2 = {1: [0.00001, 0.10, 3.625], 	2: [0.00001, 0.20, 5.5], 		3: [0.00002, 0.30, 4.75], 		4:[0.00002, 0.40, 9.5], 		5:[0.00002, 0.60, 13.5], 		6:[0.00001, 0.60, 27.125], 	7: [0.00001, 0.40, 25.375], 	8: [0.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Plant Stable Average
	run5 = {1: [0.0000001, 0.10, 8.375], 	2: [0.0000001, 0.20, 28.625], 3: [0.0000003, 0.30, 125.375],	4:[0.0000003, 0.40, 47.375], 	5:[0.0000003, 0.60, 51.0], 	6:[0.0000001, 0.60, 91.125], 	7: [0.0000001, 0.40, 63.5], 	8: [0.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Stable Average
	run6 = {1: [0.00001, 0.10, 8.375], 	2: [0.00001, 0.20, 28.625], 	3: [0.00002, 0.30, 125.375], 		4:[0.00002, 0.40, 47.375], 	5:[0.00002, 0.60, 51.0], 		6:[0.00001, 0.60, 91.125], 	7: [0.00001, 0.40, 63.5], 	8: [0.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Animal Average
	run7 = {1: [0.0000001, 0.10, 3.625], 	2: [0.0000001, 0.20, 2.375],	3: [0.0000003, 0.30, 6.625],		4:[0.0000003, 0.40, 4.125], 	5:[0.0000003, 0.60, 4.375], 	6:[0.0000001, 0.60, 10.0], 	7: [0.0000001, 0.40, 25.0], 	8: [0.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Animal Average
	run8 = {1: [0.00001, 0.10, 3.625], 	2: [0.00001, 0.20, 2.375], 	3: [0.00002, 0.30, 6.625], 		4:[0.00002, 0.40, 4.125], 	5:[0.00002, 0.60, 4.375], 	6:[0.00001, 0.60, 10.0], 		7: [0.00001, 0.40, 25.0], 	8: [0.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}

	#runs = (run1, run2, run5, run6, run7, run8)

if SICK == 0:
#this set of runs doesn't curb down the pop growth

	#run1 = {1: [1.01005, 0.10, 3.625], 	2: [1.01005, 0.20, 5.5], 	3: [1.03043, 0.30, 4.75], 		4:[1.03043, 0.40, 9.5], 	5:[1.03043, 0.60, 13.5], 	6:[1.01005, 0.60, 27.125], 	7: [1.01005, 0.40, 25.375], 8: [1.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# the new one with the pop growth expressed in percentage
# just an extra 2runs because we retreated from the pop growth equation, it's Pop Growth: HG; CC: Plant Mobile Average
	# Pop Growth: Pal; CC: Plant Mobile Average
	run0 = {1: [1.01005, 0.10, 3.625], 	2: [1.01005, 0.20, 5.5], 	3: [1.03043, 0.30, 4.75], 		4:[1.03043, 0.40, 9.5], 	5:[1.03043, 0.60, 13.5], 	6:[1.01005, 0.60, 27.125], 	7: [1.01005, 0.40, 25.375], 8: [1.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Mobile Average
	run1 = {1: [2.717, 0.10, 3.625], 	2: [2.717, 0.20, 5.5], 		3: [7.374, 0.30, 4.75], 		4:[7.374, 0.40, 9.5], 		5:[7.374, 0.60, 13.5], 		6:[2.717, 0.60, 27.125], 	7: [2.717, 0.40, 25.375], 	8: [1.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	
	# Pop Growth: Pal; CC: Plant Mobile Average
	run2 = {1: [0.00001, 0.10, 3.625], 	2: [0.00001, 0.20, 5.5], 	3: [0.00003, 0.30, 4.75], 		4:[0.00003, 0.40, 9.5], 	5:[0.00003, 0.60, 13.5], 	6:[0.00001, 0.60, 27.125], 	7: [0.00001, 0.40, 25.375], 8: [0.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Mobile Average
	run2 = {1: [0.001, 0.10, 3.625], 	2: [0.001, 0.20, 5.5], 		3: [0.002, 0.30, 4.75], 		4:[0.002, 0.40, 9.5], 		5:[0.002, 0.60, 13.5], 		6:[0.001, 0.60, 27.125], 	7: [0.001, 0.40, 25.375], 	8: [0.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Plant Mobile Maximum
	run3 = {1: [0.00001, 0.10, 8.375], 	2: [0.00001, 0.20, 11.0], 	3: [0.00003, 0.30, 23.75], 		4:[0.00003, 0.40, 20.75], 	5:[0.00003, 0.60, 33.0], 	6:[0.00001, 0.60, 53.75], 	7: [0.00001, 0.40, 41.5], 	8: [0.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Mobile Maximum
	run4 = {1: [0.001, 0.10, 8.375], 	2: [0.001, 0.20, 11.0], 	3: [0.002, 0.30, 23.75], 		4:[0.002, 0.40, 20.75], 	5:[0.002, 0.60, 33.0], 		6:[0.001, 0.60, 53.75], 	7: [0.001, 0.40, 41.5], 	8: [0.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Plant Stable Average
	run5 = {1: [0.00001, 0.10, 8.375], 	2: [0.00001, 0.20, 28.625], 3: [0.00003, 0.30, 125.375],	4:[0.00003, 0.40, 47.375], 	5:[0.00003, 0.60, 51.0], 	6:[0.00001, 0.60, 91.125], 	7: [0.00001, 0.40, 63.5], 	8: [0.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Plant Stable Average
	run6 = {1: [0.001, 0.10, 8.375], 	2: [0.001, 0.20, 28.625], 	3: [0.002, 0.30, 125.375], 		4:[0.002, 0.40, 47.375], 	5:[0.002, 0.60, 51.0], 		6:[0.001, 0.60, 91.125], 	7: [0.001, 0.40, 63.5], 	8: [0.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Animal Average
	run7 = {1: [0.00001, 0.10, 3.625], 	2: [0.00001, 0.20, 2.375],	3: [0.00003, 0.30, 6.625],		4:[0.00003, 0.40, 4.125], 	5:[0.00003, 0.60, 4.375], 	6:[0.00001, 0.60, 10.0], 	7: [0.00001, 0.40, 25.0], 	8: [0.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Animal Average
	run8 = {1: [0.001, 0.10, 3.625], 	2: [0.001, 0.20, 2.375], 	3: [0.002, 0.30, 6.625], 		4:[0.002, 0.40, 4.125], 	5:[0.002, 0.60, 4.375], 	6:[0.001, 0.60, 10.0], 		7: [0.001, 0.40, 25.0], 	8: [0.00, 0.90, 3.625], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: Pal; CC: Animal Max
	run9 = {1: [0.00001, 0.10, 8.375], 	2: [0.00001, 0.20, 4.375], 	3: [0.00003, 0.30, 12.0],		4:[0.00003, 0.40, 5.25], 	5:[0.00003, 0.60, 4.375], 	6:[0.00001, 0.60, 19.375], 	7: [0.00001, 0.40, 41.5], 	8: [0.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}
	# Pop Growth: HG; CC: Animal Maximum
	run10 = {1: [0.001, 0.10, 8.375], 	2: [0.001, 0.20, 4.375], 	3: [0.002, 0.30, 12.0], 		4:[0.002, 0.40, 5.25], 		5:[0.002, 0.60, 4.375], 	6:[0.001, 0.60, 19.375], 	7: [0.001, 0.40, 41.5], 	8: [0.00, 0.90, 8.375], 9: [0.00, 1.00, 0.00]}

runs = (run0, run2, run5, run6, run7, run8)#run3, run4, run5, run6, run7, run8, run9, run10)


def read_enviro(enviro_file):
	""" This function reads the raster file with the vegetation values """
	
	data = open(enviro_file, 'r')	
	frict_map = np.loadtxt(data) 					# load the ascii file as a numpy array 4
	data.close()
	return frict_map


def check_4_obstacles(frict_map, cellX, cellY):
	""" This function checks into how many neighbouring cells the agents can spread to """
	
	free_cells = 0
	
	if frict_map[cellX - 1, cellY] != 9:			# check for obstacles 
		free_cells += 1  							# left
	
	if frict_map[cellX + 1, cellY] != 9:
	  	free_cells += 1 							# right
	
	if frict_map[cellX, cellY + 1] != 9:
	  	free_cells += 1 							# up	
		
	if frict_map[cellX, cellY - 1] != 9:
		free_cells += 1 							# down	

	if free_cells == 0:								# to prevent division by 0
		free_cells = 1

	return free_cells

	
def diffuse(now, frict_map, runCounter, TimeCounter): 
	""" This is the core function of the simulation - it disperses the agents """
	
	next = np.zeros((X_MAX,Y_MAX), dtype = float)				# create an empty array						
	
	# iterating through the world
	for cellX in range (X_MAX - 1):
		for cellY in range (Y_MAX - 1): 	

			pop = now[cellX, cellY]									# get the value of the cell before we'll change it
			if pop > 0:
				
			# _____________READING THE ENVIRONMENT_______________ 	

				try:
					enviro = int(frict_map[cellX, cellY])				# enviro data from the friction map
				except: 
					pass
					print "the exception happened ({0}): {1}".format(e.errno, e.strerror)
				
				free_cells = check_4_obstacles(frict_map, cellX, cellY) 	# no of cells the agents can disperse to
				enviro_values = runs[runCounter]

				birth, disp_rate, cc = enviro_values[enviro]
				
			# ___________CALCULATIONS___________________
		

			# calculate how much is going to each adjecent cell
				travellers = pop * disp_rate / free_cells
				# this has been tested as well:
				#round(pop * disp_rate / free_cells)			# round is prob a better solution than integer forcing

				if travellers  == 0:							# if there's not enough people to spread then there is no spread
					disp_rate = 0 								# make sure the numbers add up further on				

			# update the cell	
				new_pop = (1 - disp_rate) * pop
				next[cellX, cellY] += new_pop									

			# update the neighbouring cells i.e. spread the agents
			  	if travellers > 0: 										# this should speed things up because the code below only for areas that actually have population
				  	if frict_map[cellX - 1, cellY] != 9:				# to prevent people from spreading into water		
			  			next[cellX - 1, cellY] += travellers; 			# left	 	

				  	if frict_map[cellX + 1, cellY] != 9:
			  			next[cellX + 1, cellY] += travellers 			# right 		  	
						
					if frict_map[cellX, cellY + 1] != 9:
			  			next[cellX, cellY + 1] += travellers			# up 

			  		if frict_map[cellX, cellY - 1] != 9:
				  		next[cellX, cellY - 1] += travellers			# down 


	#if TimeCounter % STEP == 0:
	for cellX in range (X_MAX - 1):
		for cellY in range (Y_MAX - 1): 
					
			pop = next [cellX, cellY]									# get the value of the cell before we'll change it

			if pop > 0:			

				# _____________READING THE ENVIRONMENT_______________ 	

				enviro = int(frict_map[cellX, cellY])					# enviro data from the friction map
				enviro_values = runs[runCounter]
				birth, disp_rate, cc = enviro_values[enviro]
				# _____________POP GROWTH AND CAPPING_______________ 
				new_pop =  population_growth(pop, birth, disp_rate, cc)			# population growth	+ capping to cc
				next[cellX, cellY] = new_pop

	return next

def population_growth(pop, birth, disp_rate, cc):
	pop1 = pop
	#for i in range(1000):
	#	pop =  pop + (pop * birth * (1 - (pop / cc)))		# proportion of agents remaining in original cell * no of them in the cell * birth rate	
	pop = pop + ((1 - disp_rate) * pop * birth)														# all the brackets because paranoia strikes deep
	if pop <= cc:  											# if over the carrying capacity scale down to the carrying capacity
		return pop
	else:
		return cc


def write_data(matrix, OutputCounter, runCounter, enviro_file):
    """ Writing the output into a csv file """
    
    # TO CREATE CSV FILE
    with open('results_popeq/runs' + str(runCounter)+"_time_"+ str(OutputCounter) + '.csv', 'ab') as f:
        writer = csv.writer(f)                          # use the csv writer
        writer.writerows(matrix)                        # write data
        f.close()                                       # close file
    
    # TO CREATE ASCII FILE
    OutputFile = 'results_popeq/run_'+ str(runCounter)+"_time_"+str(OutputCounter) + '.txt' 		# output file names have to differ, otherwise they will override each other
    output = open(OutputFile, 'ab')
    
    header = 'ncols         435\nnrows         265\nxllcorner     -30\nyllcorner     -60\ncellsize      0.5\nNODATA_value  -9999\n' # ascii header
    output.write(header)
    
    np.savetxt(output, matrix)							# write data
    output.close()										# close file
    
    OutputFile2 = "results_popeq/maps_numbers.txt"  # output file names have to differ, otherwise they will override each other
    output2 = open(OutputFile2, 'ab')
    text = str(OutputCounter) + '_' + str(enviro_file) + '\n'
    output2.write(text)
    output2.close()

def write_details():
	""" An extra funciton to produce a txt file with all the details of the simulation run - used to keep track of the runs"""
	output = open('details.txt', 'w')
	output.write('no of iterations {time};\n output every {st} steps; \n starting population {sp} \n'.format(time = str(MAX_TIME), st = str(STEP), sp = str(STARTING_POP))) # write the basics
	output.close()


def main(runCounter):
	""" In the main we initiate the world and iterate thorugh the diffuse procedure as the time passes """
	
	TimeCounter = 0 	                      # Standard time count
	CurveCounter = 0 				# For the climate curve list (changes every MAP CHANGE)
	VisCounter = 1 					# For the visualisations (changes every STEP)


	#_________initiate the world_____________
	matrix = np.zeros((X_MAX,Y_MAX), dtype = float) 	
	starting_cells1 = (164, 165, 166, 167)  		# initiate the point of origins for the dispersal, east Africa
	starting_cells2 = (134, 135, 136, 137)	
	
	for cell1 in starting_cells1:						# make it an area rather than one cell
		for cell2 in starting_cells2:
			matrix[cell1, cell2] = STARTING_POP	
	# Environmental curve i.e. list of maps to be uploaded, keep in mind they go in reverse order (from 2.5Ma to 0.25)
	climate = [2, 10, 11, 7, 0, 8, 12, 12, 7, 5, 8, 8, 4, 8, 11, 9, 0, 6, 9, 9, 1, 7, 11, 8, 2, 4, 12, 8, 8, 8, 11, 9, 6, 9, 12, 13, 3, 0, 8, 7, 7, 8, 12, 13, 11, 10, 10, 7, 6, 9, 11, 10, 6, 7, 11, 12, 10, 9, 9, 10, 11, 10, 10, 11, 12, 9, 10, 9, 10, 9, 11, 12, 10, 8, 8, 12, 10, 10, 10, 11, 13, 11, 10, 11, 12, 13, 11, 10, 11, 11, 8, 10, 12, 12, 10, 10, 13, 12, 10, 11, 14, 10, 8, 7, 13, 10, 5, 3, 11, 13, 9, 9, 11, 13, 10, 8, 12, 12, 12, 10, 12, 13, 10, 11, 11, 14, 7, 6, 11, 13, 13, 12, 11, 10, 9, 10, 11, 13, 13, 11, 12, 12, 11, 0, 12, 13, 14, 12, 10, 12, 12, 12, 11, 12, 13, 5, 9, 12, 14, 12, 13, 14, 15, 15, 9, 9, 10, 12, 11, 13, 15, 13, 9, 11, 13, 14, 13, 13, 15, 12, 11, 10, 13, 14, 15, 15, 16, 19, 13, 10, 11, 12, 11, 10, 13, 14, 14, 12, 12, 13, 11, 10, 11, 14, 15, 15, 16, 19, 11, 1, 0, 11, 13, 13, 14, 15, 15, 3, 5, 10, 13, 12, 12, 14, 14, 15, 9, 13, 12, 9, 9, 12, 15, 14, 16, 16, 18, 12, 0, 12, 11, 11, 11, 14, 15, 14, 14, 15, 20, 10, 0]
	fig = plt.figure()
	fig.set_size_inches(18.5,10.5)

	# passage open through straits
	enviro_file = "final_new_maps/no_straits_maps_passage_open/" + str(climate[CurveCounter]) + ".txt"  	# every STEP (eg 5 ticks) change the map for upload
	# passage closed 
	#enviro_file = "final_new_maps/yes_straits_maps_passage_close/" + str(climate[CurveCounter]) + ".txt"  
	frict_map = read_enviro(enviro_file) 					# read in the friction map for the step

	visualise(frict_map, matrix, VisCounter, runCounter, fig, TimeCounter)	
	VisCounter+= 1

	# ____________MAIN LOOP__________________
	while TimeCounter != MAX_TIME: 							# number of iterations
		
	# Friction map changing function
		if TimeCounter % MAP_CHANGE == 0:
			# passage open through straits
			enviro_file = "final_new_maps/no_straits_maps_passage_open/" + str(climate[CurveCounter]) + ".txt"  	# every STEP (eg 5 ticks) change the map for upload
			# passage closed 
			#enviro_file = "final_new_maps/yes_straits_maps_passage_close/" + str(climate[CurveCounter]) + ".txt"  
			frict_map = read_enviro(enviro_file) 					# read in the friction map for the step
			CurveCounter += 1

	# Dispersal procedures
		matrix = diffuse(matrix, frict_map, runCounter, TimeCounter)				# this is where all the shit happens
		TimeCounter +=  1 								# pass Time								
							
		
	# Write output
		if TimeCounter % STEP == 0:						# every x no of steps...			
			
			write_data(matrix, TimeCounter, runCounter, enviro_file)			    # ...write the results
			visualise(frict_map, matrix, VisCounter, runCounter, fig, TimeCounter)			# ...& ceate the visualisation
			
			print TimeCounter
			VisCounter+= 1

	write_details()	

def visualise(frict_map, matrix, VisCounter, runCounter, fig, TimeCounter):

#	
	fig.suptitle(('Run Number ' + str(runCounter)), fontsize=24, fontweight='bold')
	fig.subplots_adjust(hspace = 0.01, wspace = 0.1)
	ax = plt.subplot(5, 5, VisCounter)

	ax.imshow(frict_map, cmap= "gist_earth", zorder = 0)
	ax.imshow(matrix, cmap= "afmhot_r", zorder = 0, alpha = 0.85)
	ax.set_xticks([])                       # no axis labels
	ax.set_yticks([])
	ax.set_title("Time " + str(MAX_TIME - TimeCounter + 250) + " kya")

	file_name = 'results/results_straits/yes_straits_maps_passage_close'+ str(runCounter) + '.png'                  # save the plot to file, name = number of the time step visualised

	plt.savefig(file_name, format = 'PNG', dpi = 300)                
	#plt.show()

	
		
# ___________STARTS THE SIMULATION______________

def testing():
	runCounter = 0

	while runCounter < len(runs):

		main(runCounter)
		runCounter +=1

testing()

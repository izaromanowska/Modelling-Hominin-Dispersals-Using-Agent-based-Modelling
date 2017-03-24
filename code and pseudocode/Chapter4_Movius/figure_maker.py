import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



def make_figure(filename, fig, x, y):
	
	my_data = np.genfromtxt(filename, delimiter=',')  
	my_data[0,:] = np.array((0, 0, 0, 0, 0, 0, 0)) # it's a fake first row to make sure that the shading starts at 0, otherwise the shading looks poor
	my_data[-1,:] = np.array((160.5, 0, 0, 0, 0, 0, 0)) # it's a fake last row to make sure that the shading starts at 0, otherwise the shading looks poor

	# take data from each column
	line = my_data[:,0]
	cc1 = my_data[:,1]
	Ma_2 = my_data[:,2]
	cc2 = my_data[:,3]
	Ma_1 = my_data[:,4]
	cc3 = my_data[:,5]	
	Ma_05 = my_data[:,6]
	# specify subplots to be 3 rows one column
	gs1 = gridspec.GridSpec(3, 1)
	# enforce them into their place (yeah, I know, there must be a better way but I'm happy to wait that 20s...)
	if y == 1:
		gs1.update(left=0.55, right=0.98, wspace=0.05)
	else:
		gs1.update(left=0.05, right=0.48, wspace=0.05)
	if x == 0:
		gs1.update(bottom=0.80, top=0.95, hspace=0.05)
	elif x == 1:
		gs1.update(bottom=0.60, top=0.75, hspace=0.05)
	elif x == 2:
		gs1.update(bottom=0.40, top=0.55, hspace=0.05)
	#elif x == 3:
	#	gs1.update(bottom=0.20, top=0.35, hspace=0.05)
	#elif x == 4:
	#	gs1.update(bottom=0.00, top=0.15, hspace=0.05)

	
	#top subplot
	#ax1 = plt.subplot(3,1,1) # that would have been the other option if we went one by one throught 30 plots but then it's impossible to have different spacing between (the clusters of 3 and the rows and columns)
	ax1 = plt.subplot(gs1[0, 0])
	# plot the cc line
	plt.plot(line, cc1, '#1a9850', label = '2 Ma')
	# add the shading - it starts from whatever value is the first one so if it's not 0 it goes stupid wrong
	plt.fill(line, cc1, '#bdbdbd', alpha=0.3)
	# same for the other two ccs
	plt.plot(line, cc2, '#d7191c', label = '1 Ma')
	plt.fill(line, cc2, '#bdbdbd', alpha=0.3)
	plt.plot(line, cc3, '#2b83ba', label = '0.5 Ma')
	plt.fill(line, cc3, '#bdbdbd', alpha=0.3)

	top = int(max(max(cc1), max(cc2), max(cc3)))									# just checking the highest number
	plt.setp( ax1.get_xticklabels(), visible=False)		# no x axis labels
	ax1.set_ylim(0, top * 1.2)							# the y limit goes to slightly higher than the max value
	ax1.set_yticks([top, top * 0.5]) 					# the y ticks should go: the max value, then half + it puts 0 on anyways)
	plt.tick_params(labelsize = '8')				 	# make the ticks smaller
	#plt.legend(loc='upper right', fontsize = 4)			# add legend (probably unnecessary)

	
	#middle subplot
	#ax2 = plt.subplot(3,1,2, sharex=ax1, sharey=ax1)
	ax2 = plt.subplot(gs1[1, 0], sharex=ax1, sharey=ax1) #this one shares both x and y axis with the top one
	plt.plot(line, Ma_2, color ='#1a9850', linewidth=2.0, label='2 Ma') # apparently you need to specify the text for the legend here
	plt.plot(line, Ma_1, color ='#d7191c', linewidth=2.0, label='1 Ma')
	plt.plot(line, Ma_05, color = '#2b83ba', linewidth=2.0, label='0.5 Ma')
	#plt.legend(loc='upper right', fontsize = 4)						# add legend (probably unnecessary)
	plt.tick_params(labelsize = '8')								# make the ticks smaller

	plt.setp( ax2.get_xticklabels(), visible=False)					# use the same ticks as the subplot above (life saver...)



	#bottom subplot
	#ax3 = plt.subplot(3,1,3, sharex=ax1)
	ax3 = plt.subplot(gs1[2, 0], sharex=ax1) # it only shares the x axis
	plt.plot(line, calculate_percent (Ma_2, cc1), color = '#1a9850', linewidth=2.0, label = '2 Ma') # check if you divide them correctly
	plt.plot(line, calculate_percent (Ma_1, cc2), color = '#d7191c', linewidth=2.0, label='1 Ma')
	plt.plot(line, calculate_percent (Ma_05, cc3), color = '#2b83ba', linewidth=2.0, label='0.5 Ma')
	#plt.legend(loc='upper right', fontsize = 4)

	ax3.set_ylim(0, 105)								# the max value can only be 100 (it's a percent) so a bit of space was added
	ax3.set_yticks([100, 50, 0])						# ticks set up

	plt.tick_params(labelsize = '8') 					# makes the labels in smaller font


	plt.savefig("visual.png", format = 'PNG', dpi = 300) # save at the right resolution and format
	#plt.show()	
	fig.subplots_adjust(hspace = 1.0)					# this is where the MAGIC happens, the 3subplots get clustered properly

def calculate_percent(agents, cc):
	"auxilary function I used because I didn't believe in list comprehension - it's actually unnecessary"
	calculated = []
	for i in range(len(agents)):
		percent = agents[i] / cc[i] * 100
		if percent > 100:  # just a check
			print 'sth wrong'
		calculated.append(percent)
	return calculated

def main():
	# I didn't have the runs in 0-9 order in the picture
	filename_list = (5, 6, 1, 2, 7, 8)
	# counter for the sequence above
	file_seq = 0
	#set up the figure before the loop, otherwise you'll keep on zeroing it
	fig = plt.figure()
	# this is actually quite important because the proportions of the subplots depend on the grand size of the figure
	fig.set_size_inches(8.27,14.69)
	# 3 rows, 2 columns
	for x in range (3):
		for y in range (2):
			# pick up the right file
			filename = "results_popeq/profile_results/" + str(filename_list[file_seq]) + '.csv'
			print filename
			# do the magic
			make_figure(filename, fig, x, y)
			# follow on with the loop
			file_seq +=1





main()
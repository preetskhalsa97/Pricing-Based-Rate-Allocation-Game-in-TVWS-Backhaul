"""
Simulation of-
Ghosh, Suman, Sandip Karar, and Abhirup Das Barman. 
"A Pricing-Based Rate Allocation Game in TVWS Backhaul and Access Link for Rural Broadband."
IEEE Systems Journal 99 (2018): 1-8.
"""

"""
ASSUMPTIONS
1. utility thresholds of all UEs for a particular k are unique
"""

import math
import random
import matplotlib.pyplot as plt

def get_ue_throughput(data_rate, alpha):
	throughput = alpha + math.log(data_rate)
	return throughput

def get_optimum_ui_datarate(ki, pi):
	"""
	ki = equivalent price per unit throughput
	pi = price offered by CPEi
	"""
	return (ki/pi)

def get_optimum_cpe_utility(ki, pi, ni, P):
	"""
	ki = equivalent price per unit throughput
	pi = price offered by CPEi
	ni = number of UEs attached
	P = price offered to CPEi by CBS
	"""
	return (ni*ki*float((1-float(P/pi))))

def get_optimum_cbs_utility(ki_array, ni_array, optimum_pi_array, p):
	"""
	p = price offered by the CBS
	ki_array = array having k value for each of the CPEs
	ni_array = array having number of UEs actively being served by each of the CPEs
	optimum_pi_array = array having optimum price points offered by each of the CPEs
	"""

	if (not(len(ki_array) == len(ni_array) and len(ki_array) == lenO(optimum_pi_array))):
		raise Exception('in function "get_optimum_cbs_utility", all three arrays should have the same dimension')

	utility = 0
	for i in range(len(ki_array)):
		utility = utility + ni_array[i]*ki_array/optimum_pi_array[i]
	utility = utility * p
	return utility

def get_price_threshold(k, alpha, utility_threshold):
	# NOTE- math.exp type casts parameters to integers if none of them is float
	price_threshold = k * (math.exp(-1.0*((float(utility_threshold)/k)-alpha+1.0))) * pow(10,6) # price/Mbps
	return (price_threshold)

def get_cbs_utility(values_x, Rmax, ki_array, k2price_threshold, cpe2ue):
	# calculate the fitness of particles
	fitness = []
	for value_x in values_x:
		# value_x is a particular price of CBS
		arr = get_prices_nums_max_cpe_utility(value_x, ki_array, k2price_threshold, cpe2ue)
		optimum_prices = arr[0] # optimum prices for each CPE
		requirements = arr[1] # requirement for each CPE
		total_requirement = 0
		for requirement in requirements:
			total_requirement += requirement
			if (total_requirement > Rmax):
				total_requirement = 0 # since we want ZERO fitness here
				break
		fitness.append(value_x*total_requirement)
	return fitness

def get_prices_nums_max_cpe_utility(p, ki_array, k2price_threshold, cpe2ue):
	# CHECK THIS FUNCTION MANUALLY
	"""
	p = price offered by CBS
	ki_array = array containing ki for each of the CPEs
	returns ans = [[<optimum prices for each CPE>],[<total data required for each CPE>]]
	"""
	optimum_prices = []
	requirement = []
	# for each of the CPE, we will check the CPE utility at the threshold prices of the respective ki values
	# threshold price for which utility maximizes is the resultant pi for that CPE
	for i in range(len(ki_array)):
		# print ('for CPI '+str(i))
		k = ki_array[i] # k for this CPE
		n_ui = cpe2ue[i+1] # number of UIs available for this CPE
		price_thresholds = (k2price_threshold[k])[0:n_ui] # we need to test for each of these thresholds

		max_CPE_utility = None # CHANGED FROM 0
		optimum_price = None
		n_at_max_CPE_utility = None

		for j in range(len(price_thresholds)):
			this_price = price_thresholds[j] # was i earlier!!! :/
			update = 0
			this_utility = get_optimum_cpe_utility(k, this_price, n_ui - j, p)
			# print ('utility for '+str(this_price)+' = '+str(this_utility))
			# print ('max_CPE_utility = '+str(max_CPE_utility))
			if (max_CPE_utility == None):
				# print ("max_CPE_utlity NONE")
				update = 1
			else:
				if (max_CPE_utility < this_utility):
					# print ('max_CPE_utility < this_utility')
					update = 1
			if (update != 0):
				# print ('updating max variables')
				max_CPE_utility = this_utility
				n_at_max_CPE_utility = n_ui-j
				optimum_price = this_price			

		Ri = n_at_max_CPE_utility*k/optimum_price

		#DOUBT-- will it operate under a loss?! ==> NO <PSK>, since if so, CBS can give infinitely high price!!
		# requirement.append(Ri)

		# print (max_CPE_utility)

		if(max_CPE_utility < 0):
			requirement.append(0)
			# print ('requirement = '+str(0))
		else:
			requirement.append(Ri)
			# print ('requirement = '+str(Ri))
				
		optimum_prices.append(optimum_price)
		# print ('optimum_price'+str(optimum_price))

	ans = []
	ans.append(optimum_prices)
	ans.append(requirement)
	return ans

#initializing values given in the paper
alpha = 1

# utility thresholds -->  corresponding price thresholds in unit/bps
k_point5 = [7.5, 7.1, 6.7, 6.3, 5.9, 5.5]
k_1 = [15.5, 14.7, 13.9, 13.1, 12.3, 11.6]
k_2 = [31, 29.7, 28.4, 27.1, 25.8, 24.5]
k_3 = [48, 46, 44, 42, 40, 38]
k_4 = [65, 62.6, 60.2, 57.8, 55.4, 53]
k2utility_thresholds = {0.5:k_point5, 1:k_1, 2:k_2, 3:k_3, 4:k_4}

# finding price thresholds for each k
k2price_threshold = {}
for k in k2utility_thresholds:
	arr = []
	for element in k2utility_thresholds[k]:
		arr.append(get_price_threshold(k, alpha, element)) # prices in uni/mbps
	k2price_threshold[k] = arr

# print (k2price_threshold)

n_cpe = 4 # number of customer premises equipment = #clusters
cpe2ue = {1:5, 2:3, 3:4, 4:6} # mapping numbeer of user equipment to each cpe (indexed -- 1, 2, 3, 4)

#range for prices -- everything in unit/Mbps
cpe_price_low = 0.1 
cpe_price_high = 10
cbs_price_low = 0.01
cbs_price_high = 100

Rmax =240 # Mbps

ki_array = [4, 4, 4, 4]

# carry out PSO for CBS price optimization; for evaluating resulting prices and requirements of each CPE, use func get_prices_nums_max_cpe_utility

max_iter = 30000
w = 0.01
c1 = 0.7 # exploratory
c2 = 1.5 # global --> converging
speed_const = 0.1

# finding the upper and lower limits of movement of CBS price
# logically, CBS price cannot increase the highest threshold price, so lower_limit = 0, upper_limit = highest_threshold_price
lower_limit = 0
upper_limit = 0
for i in range(len(ki_array)):
	threshold_price_arr = k2price_threshold[k][0:cpe2ue[i+1]]
	this_max = max(threshold_price_arr)
	if (this_max > upper_limit):
		upper_limit = this_max

print ("upper_limit = " + str(upper_limit))

vmax = speed_const*(upper_limit - lower_limit)
v_limit = int(vmax) + 1
no_particles = 300

values_x = [] # position of each price point
velocity = [] # velocity of each point for every iteration
p_best_x = [] # personal best of each point
g_best_x   = random.randrange(0, int(upper_limit) + 1)  #global best x_value -- initiated to a random value, lower bound 1 since HAS to be an int
g_best_y = (get_cbs_utility([g_best_x], Rmax, ki_array, k2price_threshold, cpe2ue))[0]
#assign uniform positions and random velocities to the particles
for i in range(no_particles):
    values_x.append(random.uniform(lower_limit, upper_limit))
    velocity.append(random.randrange(-1*v_limit, v_limit)) # CHANGING from random

p_best_x = values_x[::] # making a copy, NOT a reference
p_best_y = get_cbs_utility(p_best_x, Rmax, ki_array, k2price_threshold, cpe2ue) # resultant CBS utility of each personal best pt

# print (p_best_x)
# print (p_best_y)

# simulating PSO

for j in range(max_iter):

	# print j
	# calculate the fitness of particles
	fitness = get_cbs_utility(values_x, Rmax, ki_array, k2price_threshold, cpe2ue) # fitness vector corresponding to values_x
	
	# upadate personal best array
	# we want to MAXIMIZE utility

	for i in range(len(fitness)):
		if (fitness[i] > p_best_y[i]):
			# update
			p_best_x[i] = values_x[i]
			p_best_y[i] = fitness[i]

			if (fitness[i] > g_best_y):
				g_best_x = values_x[i]
				g_best_y = (get_cbs_utility([g_best_x], Rmax, ki_array, k2price_threshold, cpe2ue))[0]

	# UPDATING velocity and hence, position of particles for the next iteration

	for i in range(len(values_x)):
		r1 = random.random()
		r2 = random.random()

		#calculate new velocity and set it in the [min, max] range
		velocity[i] = w*velocity[i] + c1*r1*(p_best_x[i] - values_x[i]) + c2*r2*(g_best_x - values_x[i])
		if (velocity[i] > vmax):
			velocity[i] = vmax
		if(velocity[i] < -1*vmax):
			velocity[i] = -1*vmax

		#calculate new positions and set it in the [min, max] range
		values_x[i] = values_x[i] + velocity[i]
		if (values_x[i] > upper_limit):
			values_x[i] = upper_limit
		if (values_x[i] < lower_limit):
			values_x[i] = lower_limit

for value_x in values_x:
	# positions of all the particles at the end of the PSO
	print value_x
print ('.........')
# print (k2price_threshold)
# print (values_x[0])
print ('utility of the converged point')
print (get_cbs_utility([values_x[0]], Rmax, ki_array, k2price_threshold, cpe2ue)) # utility of all the particles
print ('[[<optimum prices for each CPE>],[<total data required for each CPE>]]')
print (get_prices_nums_max_cpe_utility(values_x[0], ki_array, k2price_threshold, cpe2ue))


"""
NOT CONVERGING?? <not anymore :) >
plot price range on the x axis and utility on the y axis ==> Constant curve @ 0 across all prices!!

start = 0.01
end = 100
x = start
y_arr = []
x_arr = []

while (x<=end):
	x_arr.append(x)
	x+=0.01

y_arr = get_cbs_utility(x_arr, Rmax, ki_array, k2price_threshold, cpe2ue)

plt.plot(x_arr, y_arr)
while True:
    plt.pause(0.05)

print (k2price_threshold[4])
"""
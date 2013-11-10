mport socket
import random
import sys
import numpy
import pdb

#def send(msg):
#    print "sending"
#    print msg
#    msg += "\n<EOM>\n"
#    totalsent = 0
#    while totalsent < len(msg):
#        sent = s.send(msg[totalsent:])
#        if sent == 0:
#            raise RuntimeError("socket connection broken")
#        totalsent = totalsent + sent
#
#def receive():
#    msg = ''
#    while '<EOM>\n' not in msg:
#        chunk = s.recv(1024)
#        if not chunk: break
#        if chunk == '':
#            raise RuntimeError("socket connection broken")
#        msg += chunk
#    msg = msg[:-7]
#    return msg

def randomInt(num):
	return(random.randint(0, num - 1))

def high_skew_rand(skew_num, zero_num, skew_amt, weights):
	skews = []
	zeroes = []
	min = 1
	r = 0
	tmp = 0
	
	for x in range(0,skew_num):
		r = randomInt(n)
		skews.append(r)
	for x in range(skew_num, skew_num + zero_num):
		r = randomInt(n)
		while(r in skews):
			r = randomInt(n)
		zeroes.append(r)
	
	for x in range(0,n):
		if(x < n /2):
			weights.append(min)
		else:
			weights.append(-1 * min)
			
	random.shuffle(weights)
	
	for x in range(0,n):
		if(x in skews):
			if(weights[x] > 0):
				weights[x] = weights[x] + skew_amt * min
			elif(weights[x] < 0):
				weights[x] = weights[x] - skew_amt * min
		elif(x in zeroes):
			weights[x] = 0
	
	random.shuffle(weights)
			
def uniform(n, num_zero, weights):
	min = 100 / (n - num_zero)
	
	for x in range(0, num_zero):
		weights.append(0)
	for x in range(num_zero,n):
		if (x < ((n - num_zero)/2)+num_zero and x >= num_zero):
			weights.append(min)
		elif(x >= ((n - num_zero)/2) + num_zero):
			weights.append(-1 * min)
	
	random.shuffle(weights)
	
def determine_sign(num):
	if (num > 0):
		return 1
	elif (num < 0):
		return 0
	else:
		return 1
	
def random_choice_to_mod(n, possible_mod, orig, weights):
	num_change_max = n / 20
	rands = []
	r = -1
	flag = True
	flag2 = True
	to_change = randomInt(n)
	up_or_down = randomInt(10) % 2
	change = random.randint(1,num_change_max - 1)
	possibles = []
	
	counter = 0
	while(possible_mod[to_change][up_or_down] == 0):
		counter = counter + 1
		to_change = randomInt(n)
		if(counter > 1000):
			return (-1, -1, [], False)

	for i in range(0, len(possible_mod), 2):
		if(i != to_change and possible_mod[i][up_or_down] != 0):
			possibles.append(i)
	
	print "Chosen to mod: ", to_change
	print "Its original value: ", orig[to_change]
	print "Its possible mod: ", possible_mod[to_change]
		
	is_pos = determine_sign(orig[to_change])
	is_pos2 = -1
	counter = 0
	
	if(len(possibles) == 0):
		return(-1, -1, [], False)
	
	while(flag == True):
		rands = []
		sum = 0
		n = -1
		for i in range(0, change):
			num = random.randint(0, len(possibles) - 1)
			r = possibles[num]
			possibles.pop(num)
			rands.append(r)
			#print rands
		counter = counter + 1
		if(counter > 100000):
			return (-1, -1, [], False)
		for i in range(0, len(rands)):
			sum = sum + possible_mod[rands[i]][up_or_down]
		if (sum >= possible_mod[to_change][up_or_down]):
			flag = False
	
	if(len(rands) == 0):
		return(-1, -1, [], False)
		
	print "Others chosen to mod: ", rands
	for x in rands:
		print "Values: ", orig[x]
	print "Sum: ", sum
	
	return(to_change, up_or_down, rands, True)
	
def random_mod(n, possible_mod, orig, weights):
	add_or_subtract = -1
	amt = 0
	
	a = random_choice_to_mod(n, possible_mod, orig, weights)
	to_change = a[0]
	up_or_down = a[1]
	rands = a[2]
	possible = a[3]
	
	if(possible == False):
		return False

	amt = possible_mod[to_change][up_or_down]
	amt = random.randint(1, amt)
	print "AMOUNT", amt
	possible_mod[to_change][up_or_down] = (possible_mod[to_change][up_or_down] - 1)
	
	sum = 0
	r = -1

	while(sum != amt):
		r = randomInt(len(rands))
		if (up_or_down == 1 and possible_mod[rands[r]][up_or_down] > 0):
			if(weights[rands[r]] > 0):
				weights[rands[r]] = weights[rands[r]] + 1
				sum = sum + 1
			elif(weights[rands[r]] < 0):
				weights[rands[r]] = weights[rands[r]] - 1
				sum = sum + 1
		elif(up_or_down == 0 and possible_mod[rands[r]][up_or_down] > 0):
			if(weights[rands[r]] > 0):
				weights[rands[r]] = weights[rands[r]] - 1
				sum = sum + 1
			elif(weights[rands[r]] < 0):
				weights[rands[r]] = weights[rands[r]] + 1
				sum = sum + 1
		determine_mod(n, possible_mod, orig, weights)
	
	#print possible_mod
	
	# at end, change possible mod appropriately
	print possible_mod
	
#modify this to be able to determine mod based on original values and current state
def determine_mod(n, possible_mod, orig, weight):
	#note: increase is defined as increasing the absolute value
	max_increase = 0
	max_decrease = 0
	current_change = 0
	
	del possible_mod[:]
		
	for i in range(0, n):
		a = []
		current_change = weight[i] - orig[i]
		#print "CURRENT CHANGE ", current_change
		if(abs(weight[i]) < 5):
			max_increase = 0
			max_decrease = 0
		elif(weight[i] > 0):
			if(current_change > 0):
				max_increase = (orig[i] / 5) - current_change
				max_decrease = (orig[i] / 5) + current_change
			elif(current_change < 0):
				max_increase = (orig[i] / 5) + abs(current_change)
				max_decrease = (orig[i] / 5) - abs(current_change)
			else:
				max_increase = (orig[i] / 5)
				max_decrease = (orig[i] / 5)
		elif(weight[i] < 0):
			if(current_change > 0):
				max_increase = abs((orig[i] / 5)) + abs((current_change))
				max_decrease = abs((orig[i] / 5)) - abs((current_change))
			elif(current_change < 0):
				max_increase = abs((orig[i] / 5)) - abs(current_change)
				max_decrease = abs((orig[i] / 5)) + abs(current_change)
			else:
				max_increase = abs((orig[i] / 5))
				max_decrease = abs((orig[i] / 5))
		a.append(abs(max_increase))
		a.append(abs(max_decrease))
		#a = abs(max_increase), abs(max_decrease)
		possible_mod.append(a)

		
	#print possible_mod
	#print weights
	
	#make sure the weight array is still ints at the moment.
	#for i in range(0, n):
	#	possible_mod.append((abs(weight[i]) / 5))
		
def fix_values(weights):
	for i in range(0,len(weights)):
		weights[i] = float(int(weights[i])) / 100.0
		
def back_to_int(weights):
	for i in range(0, len(weights)):
		weights[i] = int(weights[i] * 100)

def sum_values(weights):
	pos_sum = 0
	neg_sum = 0
	for i in range(0,n):
		if(weights[i] > 0):
			pos_sum = pos_sum + weights[i]
		elif(weights[i] < 0):
			neg_sum = neg_sum + weights[i]
			
	return(pos_sum, neg_sum)

def fix_sums_random(weights):
	pos_sum = 0.0
	neg_sum = 0.0
	r = 0
	min = 1
	a = sum_values(weights)
	pos_sum = a[0]
	neg_sum = a[1]
	for i in range(0,n):
		if(weights[i] > 0):
			pos_sum = pos_sum + weights[i]
		elif(weights[i] < 0):
			neg_sum = neg_sum - weights[i]
	while(pos_sum != 100):
		r = randomInt(n)
		if(weights[r] > 0 and pos_sum > 100):
			weights[r] = weights[r] - min
		elif(weights[r] > 0 and pos_sum < 100):
			weights[r] = weights[r] + min
		a = sum_values(weights)
		pos_sum = a[0]
	while(neg_sum != -100):
		r = randomInt(n)
		if(weights[r] < 0 and neg_sum > -100):
			weights[r] = weights[r] - min
		elif(weights[r] < 0 and neg_sum < -100):
			weights[r] = weights[r] + min
		pos_sum = 0
		neg_sum = 0
		a = sum_values(weights)
		neg_sum = a[1]
		
def fix_sums_uniform(weights):
	pos_sum = 0.0
	neg_sum = 0.0
	r = 0
	min = 1
	a = sum_values(weights)
	pos_sum = a[0]
	neg_sum = a[1]
	for i in range(0,n):
		if(weights[i] > 0):
			pos_sum = pos_sum + weights[i]
		elif(weights[i] < 0):
			neg_sum = neg_sum - weights[i]
	while(pos_sum != 100):
		if(weights[r] > 0 and pos_sum > 100):
			weights[r] = weights[r] - min
		elif(weights[r] > 0 and pos_sum < 100):
			weights[r] = weights[r] + min
		a = sum_values(weights)
		pos_sum = a[0]
		r = (r + 1) % n

	r = 0
	while(neg_sum != -100):
		if(weights[r] < 0 and neg_sum > -100):
			weights[r] = weights[r] - min
		elif(weights[r] < 0 and neg_sum < -100):
			weights[r] = weights[r] + min
		pos_sum = 0
		neg_sum = 0
		a = sum_values(weights)
		neg_sum = a[1]
		r = (r + 1) % n		
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(('127.0.0.1', int(sys.argv[1])))
#send("TEAM")

n = int(sys.argv[2])
t_or_f = True
current_mod = []
possible_mod = []
weights = []
for i in range(0,n):
	current_mod.append(0)
#high_skew_rand(5, 5, 14, weights)
uniform(n, 0, weights)
orig = weights[:]
#determine_mod(n, possible_mod, orig, weights)
#random_mod(n, possible_mod, orig, weights)
#t_or_f = random_mod(n, possible_mod, orig, weights)
#fix_sums_uniform(weights)
#fix_values(weights)
#back_to_int(weights)
fix_sums_random(weights)
fix_values(weights)

#print "FIRST WEIGHTS ", weights
#t_or_f = modify_values_random(n, current_mod, orig, weights)
#print "SECOND WEIGHTS ", weights
a = sum_values(weights)
print "FINAL_WEIGHTS", weights
print "current_mod:"
#print current_mod
print "Pos sum =" + str(a[0])
print "Neg sum =" + str(a[1])

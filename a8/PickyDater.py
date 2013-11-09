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
#
def randomInt(num):
	return(random.randint(0, num - 1))

#revise this to make it MOAR RANDOM
def high_skew_rand(skew_num, zero_num, skew_amt, weights):
	skews = []
	zeroes = []
	min = 1
	r = 0
	tmp = 0
	
	for x in range(0,skew_num):
		skews.append(x)
	for x in range(skew_num, skew_num + zero_num):
		zeroes.append(x)
	for x in range(0, skew_num):
		r = random.randint(0, skew_num - 1)
		tmp = skews[r]
		skews[r] = skews[x]
		skews[x] = tmp
	for x in range(0, zero_num):
		r = random.randint(0, zero_num - 1)
		tmp = zeroes[r]
		zeroes[r] = zeroes[x]
		zeroes[x] = tmp
	
	for x in range(0,n):
		if(x < n /2):
			weights.append(min)
		else:
			weights.append(-1 * min)
		if(x < skew_num and skews[x] < skew_num / 2):
			weights[x] = weights[x] + skew_amt * min
		elif(x < skew_num and skews[x] > skew_num / 2):
			weights[x] = weights[x] - skew_amt * min
		if(x < zero_num):
			weights[x] = 0;
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
	
def modify_values_random(n, orig, weights):
	a = choose_rand_to_mod(n,orig, weights)
	mod = a[0]
	rands = a[1]
	possible = a[2]
	modifier = a[3]
	modifier = int(modifier * 100)
	modifier = random.randint(0,modifier)
	modifier = float(modifier / 100.0)
	
	print orig[mod]
	print rands
	print possible
	print modifier
	
	if(possible == False):
		return False
		
	# FINISH THIS!!!
	
	
def choose_rand_to_mod(n, orig, weights):
	num_change_max = n / 20
	r = randomInt(n)
	modifier = .2
	change = 0
	sum = 0
	count = 0
	counter = 0
	rands = []
	possible = True
	
	while(orig[r] < .05):
		r = randomInt(n)
	
	while(change < 2):
		change = random.randint(0,num_change_max)
	
	while((1.2 * sum < (1 + modifier) * abs(orig[r])) and possible == True):
		sum = 0
		rands = []
		for i in range(0, change - 1):
			rand = randomInt(n)
			while(rand in rands or rand == r or orig[rand] < .05):
				rand = randomInt(n)
				counter = counter + 1
				if(counter > 1000):
					possible = False
					break
				#print rand
			rands.append(rand)
			sum = sum + abs(orig[rands[i]])
		count = count + 1
		if(count % 10 == 0):
			modifier = modifier - .01
		if(modifier < 0):
			possible = False
			break
		#print modifier
		#print "ABS: " + str(abs(orig[r]))
		#print "SUM: " + str(sum)
	#print r
	#print rands

	return(r, rands, possible, modifier)
	
	
	
	
		
	#function that changes at most 5% of the values
	#such that they differ only up to 20% from their
	#original value. We have to make sure that if we
	#change a value, the number of other values we 
	#have to adjust in order for them to sum up to 1
	#is not more than 5% of the total number of values.
	
	
def fix_values(weights):
	for i in range(0,len(weights)):
		weights[i] = float(int(weights[i])) / 100.0

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
weights = []
high_skew_rand(8, 0, 4, weights)
fix_sums_random(weights)
#uniform(n, 3, weights)
#fix_sums_uniform(weights)
fix_values(weights)
orig = weights[:]
modify_values_random(n, orig, weights)
a = sum_values(weights)
print weights
print "Pos sum =" + str(a[0])
print "Neg sum =" + str(a[1])

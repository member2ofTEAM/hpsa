import socket
import random
import sys
import numpy
import pdb
import math

def send(msg):
    print "sending"
    print msg
    msg += "<EOM>\n"
    totalsent = 0
    while totalsent < len(msg):
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def receive():
    msg = ''
    while '<EOM>' not in msg:
        chunk = s.recv(1024)
        if not chunk: break
        if chunk == '':
            raise RuntimeError("socket connection broken")
        msg += chunk
    msg = msg[:-6]
    return msg

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
        if (x < (n /2)+num_zero and x >= num_zero):
            weights.append(min)
        elif(x >= (n /2) + num_zero):
            weights.append(-1 * min)
    #print sum_values(n, weights) 
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

    #print "Chosen to mod: ", to_change
    #print "Its original value: ", orig[to_change]
    #print "Its possible mod: ", possible_mod[to_change]
    #print "Possibles:", possibles
		
    is_pos = determine_sign(orig[to_change])
    is_pos2 = -1
    counter = 0

    if(len(possibles) == 0):
        return(-1, -1, [], False)


    change = min(len(possibles),change)

    while(flag == True):
        rands = []
        sum = 0
        n = -1
        tmp = possibles[:]
        #pdb.set_trace()
        for i in range(0, change):
            if(len(tmp) == 1):
               num = 0
            elif(len(tmp) == 0):
               return(-1, -1, [], False)
            else:
               num = random.randint(0, len(tmp) - 1)
            r = tmp[num]
            tmp.pop(num)
            is_pos2 = determine_sign(orig[r])
            if(is_pos == is_pos2):
                rands.append(r)
        counter = counter + 1
        if(counter > 100000):
            return (-1, -1, [], False)
        for i in range(0, len(rands)):
            sum = sum + possible_mod[rands[i]][up_or_down]
        if (sum >= possible_mod[to_change][up_or_down]):
            flag = False

    if(len(rands) == 0):
        return(-1, -1, [], False)
	
    #print "Others chosen to mod: ", rands
    #for x in rands:
    #    print "Values: ", orig[x]
    #print "Sum: ", sum

    return(to_change, up_or_down, rands, True)
	
def random_mod(n, possible_mod, orig, weights):
    add_or_subtract = -1
    amt = 0
	
    a = random_choice_to_mod(n, possible_mod, orig, weights)
    to_change = a[0]
    up_or_down = a[1]
    rands = a[2]
    possible = a[3]

    #pdb.set_trace()
    #print "Possibles to mod: ", rands
    #there's an error here somewhere

    #print possible
    if(possible == False):
        return False

    amt = possible_mod[to_change][up_or_down]
    amt = random.randint(1, amt)
    #print "AMOUNT", amt
    if(up_or_down == 1):
        weights[to_change] = weights[to_change] + amt
    elif(up_or_down == 0):
        weights[to_change] = weights[to_change] - amt
	
    sum = 0
    r = -1
    
    while(sum != amt):
        r = randomInt(len(rands))
        if (up_or_down == 1 and possible_mod[rands[r]][up_or_down] > 0):
            if(weights[rands[r]] > 0):
                weights[rands[r]] = weights[rands[r]] - 1
                sum = sum + 1
            elif(weights[rands[r]] < 0):
                weights[rands[r]] = weights[rands[r]] - 1
                sum = sum + 1
        elif(up_or_down == 0 and possible_mod[rands[r]][up_or_down] > 0):
            if(weights[rands[r]] > 0):
                weights[rands[r]] = weights[rands[r]] + 1
                sum = sum + 1
            elif(weights[rands[r]] < 0):
                weights[rands[r]] = weights[rands[r]] + 1
                sum = sum + 1
        #determine_mod(n, possible_mod, orig, weights)

    # at end, change possible mod appropriately
    #print possible_mod
	

def determine_mod(n, possible_mod, orig, weight):
    #note: increase is defined as increasing the absolute value
    max_increase = 0
    max_decrease = 0
    current_change = 0
 
    del possible_mod[:]
   
    #print weight
    #print orig
    for i in range(0, n):
        a = []
        current_change = weight[i] - orig[i]
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
                max_increase = abs((orig[i] / 5))
                max_decrease = abs((orig[i] / 5))
        elif(weight[i] < 0):
            if(current_change > 0):
                max_increase = abs((orig[i] / 5)) + abs((current_change))
                max_decrease = abs((orig[i] / 5)) - abs((current_change))
            elif(current_change < 0):
                max_increase = abs((orig[i] / 5)) - abs(current_change)
                max_decrease = abs((orig[i] / 5)) + abs(current_change)
            else:
                max_increase = abs((abs(orig[i]) / 5))
                max_decrease = abs((abs(orig[i]) / 5))
        a.append(abs(max_increase))
        a.append(abs(max_decrease))
        #a = abs(max_increase), abs(max_decrease)
        possible_mod.append(a)
    #print possible_mod

def fix_values(weights):
    pdb.set_trace()
    a = 0
    b = 0
    for i in range(0,len(weights)):
        weights[i] = float(int(weights[i])) / 100.0
        weights[i] = str(round(weights[i], 2))
	weights[i] = float(weights[i])
        a = 5
        b = 6

def back_to_int(weights):
    for i in range(0, len(weights)):
        weights[i] = int(weights[i] * 100.0)

def sum_values(n, weights):
    pos_sum = 0
    neg_sum = 0
    for i in range(0,n):
        if(weights[i] > 0):
            pos_sum = pos_sum + weights[i]
        elif(weights[i] < 0):
            neg_sum = neg_sum + weights[i]
		
    return(pos_sum, neg_sum)

def fix_sums_random(n, weights):
    pos_sum = 0.0
    neg_sum = 0.0
    r = 0
    min = 1
    a = sum_values(n, weights)
    pos_sum = a[0]
    neg_sum = a[1]
    while(pos_sum != 100):
        r = randomInt(n)
        if(weights[r] > 0 and pos_sum > 100):
            weights[r] = weights[r] - min
        elif(weights[r] > 0 and pos_sum < 100):
            weights[r] = weights[r] + min
        a = sum_values(n, weights)
        pos_sum = a[0]
    while(neg_sum != -100):
        r = randomInt(n)
        if(weights[r] < 0 and neg_sum > -100):
            weights[r] = weights[r] - min
        elif(weights[r] < 0 and neg_sum < -100):
            weights[r] = weights[r] + min
        pos_sum = 0
        neg_sum = 0
        a = sum_values(n, weights)
        neg_sum = a[1]

def fix_sums_uniform(n, weights):
    pos_sum = 0.0
    neg_sum = 0.0
    r = 0
    min = 1
    a = sum_values(n, weights)
    pos_sum = a[0]
    neg_sum = a[1]
    while(pos_sum != 100):
        if(weights[r] > 0 and pos_sum > 100):
            weights[r] = weights[r] - min
        elif(weights[r] > 0 and pos_sum < 100):
            weights[r] = weights[r] + min
        a = sum_values(n, weights)
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
        a = sum_values(n, weights)
        neg_sum = a[1]
        r = (r + 1) % n		

def construct_string(weights):
    string = ''
    pos_sum = 0
    neg_sum = 0
    for i in range(0, len(weights)):
        if(weights[i] == 0):
            string = string + '0.00' + ' '
        else:
            tmp = float(int(weights[i])) / 100.0
            ceil = math.ceil(tmp)
            if(abs(ceil - tmp) <= .005):
                tmp = str(ceil)
            elif(abs(ceil - tmp) > .005):
                tmp = str(math.floor(tmp))
            #tmp = str(round(tmp, 2))
            if(float(tmp) > 0):
                pos_sum = pos_sum + float(tmp)
            elif(float(tmp) < 0):
                neg_sum = neg_sum + float(tmp)
            string = string + tmp + ' '
    string = string + '\n'
    #print pos_sum, neg_sum
    #print "Inside construct_string " + string
    return string

def construct_string2(weights):
    string = ''
    for i in range(0, len(weights)):
        if(weights[i] == 0):
            string = string + '0.00' + ' '
        elif(abs(weights[i]) > 0 and abs(weights[i]) < 10):
            if(weights[i] < 0):
                string = string + '-0.0' + str(abs(weights[i])) + ' '
            elif(weights[i] > 0):
                string = string + '0.0' + str(abs(weights[i])) + ' '
        elif(abs(weights[i]) >= 10):
            if(weights[i] < 0):
               string = string + '-0.' + str(abs(weights[i])) + ' '
            elif(weights[i] > 0):
               string = string + '0.' + str(abs(weights[i])) + ' '
    string = string + '\n'
    return string


if __name__ == "__main__":
    name = "TEAM"
    possible_mod = []
    weights = []
    t_or_f = True
    to_send = ''
    
    #pdb.set_trace()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    if (len(sys.argv)) == 3:
        random.seed(int(sys.argv[2]))
		
    msg = receive()

    if(msg == "Team Name?"):
        send(name)

	
    msg = receive()
    msg = msg.split(' ')
    n = int(msg[1])

    #decide which type of weights we will generate

    #high_skew_rand(5, 3, 4, weights)
    uniform(n, 0, weights)
    

    #fix_sums_uniform(n, weights)
    fix_sums_random(n, weights)    

    orig = weights[:]
    
    #stores original weights and determines how much they can be modified by
    determine_mod(n, possible_mod, orig, weights)

    #t_or_f = random_mod(n, possible_mod, orig, weights)


    #fix the values by making them floats
    #fix_values(weights)

    #pdb.set_trace()
    #print orig
    to_send = construct_string2(weights)
    to_send = to_send + "\n"
    #print to_send
    #print sum_values(n, weights)
    send(to_send)
   
    while(1):
        to_send = ''
        msg = receive()
       # pdb.set_trace()
        if(msg == "next weights?"):
            #back_to_int(weights)
            del weights[:]
            weights = orig[:]
            t_or_f = random_mod(n, possible_mod, orig, weights)
            #fix_values(weights)
                #for i in range(0, len(weights)):
                #    to_send = to_send + " " + str(weights[i])
            to_send = construct_string2(weights)
                #for i in range(0, len(weights)):
                #    to_send = to_send + " " + str(weights[i])
                #do some other sort of modification or something
            #pdb.set_trace()
            
           # print orig
           # print weights
           # print possible_mod
           # print sum_values(n, weights)
           # print "check" + to_send
            send(to_send)
		
        #a = sum_values(weights)
        #print "FINAL_WEIGHTS", weights
        #print "current_mod:"
        #print current_mod
        #print "Pos sum =" + str(a[0])
        #print "Neg sum =" + str(a[1])


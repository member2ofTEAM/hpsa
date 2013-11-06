import socket
import random
import sys
import pdb
import time
import numpy as np
from sklearn.linear_model import LinearRegression

def send(msg):
    print "sending"
    print "Send: " + msg
    totalsent = 0
    while totalsent < len(msg):
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def receive():
    msg = ''
    while (1):
        chunk = s.recv(1024)
        if not chunk: break
        if chunk == '':
            raise RuntimeError("socket connection broken")
        msg += chunk
    msg = msg[:-7]
    return msg

def parse_data(data):
    data = data.split("\n")
    init = data[0]
    rest = data[1:]
    n = int(init.split(" ")[1])
    pre_data = n*[0]
    for i in range(n):
        pre_data[i] = map(int, rest[i].split(" "))
    return (n, np.array(pre_data))

def parse_update(data):
    data = data.split("\n")
    update = data[-1]
    update = map(int, update.split(update, " "))
    return update

#Create list of length n with i sublists alternating between 0 and 1
def i_zeros(n, i):
    last = n % i
    rest = n / i
    result = []
    for j in range(firsts):
        if j % 2:
            result.append([1] * rest)
        else:
            result.append([0] * rest)
    result.append(last * [1])
    #flatten the result
    return [item for sublist in result for item in sublist]

   
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    send("TEAM")
    pdb.set_trace()
    (n, init_data) = parse_data(receive())
    clf = LinearRegression()
    for i in range(20):
        clf.fit(init_data[:,:-1], init_data[:,-1])
        print clf.coef_
        init_data.append(parse_update(receive(), axis=1)
    

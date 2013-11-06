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
    msg += "<EOM>\n"
    totalsent = 0
    while totalsent < len(msg):
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent

def receive():
    msg = ''
    while '<EOM>\n' not in msg:
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
    pre_data = 20*[0]
    for i in range(20):
        pre_data[i] = map(float, rest[i].split(" ")[:-1])
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
    for j in range(i):
        if j % 2:
            result.append([1] * rest)
        else:
            result.append([0] * rest)
    if last:
        result.append(last * [1])
    #flatten the result
    return [item for sublist in result for item in sublist]

   
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    receive()
    pdb.set_trace()
    send("TEAM")
    (n, init_data) = parse_data(receive())
    clf = LinearRegression()

    for i in range(19):
        clf.fit(init_data[:, :-1], init_data[:,-1])
        w = clf.coef_
        zeros = ""
        for zero in i_zeros(n, i + 2):
            zeros += str(zero) + " "
        zeros = zeros[:-1]
        send(zeros)
        update = parse_update(receive())
        init_data.append(update, axis=1)

    candidate = n * [0]
    for i in range(len(w)):
        if w[i] > 0:
            candidate[i] = 1


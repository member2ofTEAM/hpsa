import socket
import random
import sys
import pdb
import time
import numpy as np
from sklearn.linear_model import LinearRegression, BayesianRidge


def send(msg):
    print "sending"
    print "Send: " + msg
    msg += '<EOM>\n'
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
    update = map(float, update.split(" ")[:-1])
    return update

#Create list of length n with i sublists alternating between 0 and 1
def i_zeros(n, i):
    app = 1
    if i % 2:
        app = 0
    i = i / 2
    last = n % i
    rest = n / i
    result = []
    for j in range(i):
        if j % 2:
            result.append([int(app)] * rest)
        else:
            result.append([int(not app)] * rest)
    if last:
        if i % 2:
            result.append(last * [int(app)])
        else:
            result.append(last * [int(not app)])
    #flatten the result
    result = [item for sublist in result for item in sublist]
    assert len(result) == n
    return result

   
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    if (len(sys.argv)) == 3:
        random.seed(int(sys.argv[2]))
        np.random.seed(int(sys.argv[2]))
    receive()
    send("TEAM")
    (n, init_data) = parse_data(receive())
    if n <= 40:
        clf = LinearRegression(fit_intercept=False)
    else:
       clf = BayesianRidge(fit_intercept=False)
    get_weight = lambda: clf.coef_
    
    if n <= 40:
        size_b = 3000
    else:
        size_b = 2500
    ws = size_b * [0]
    for i in range(19):
        if i > 0:
            train_index = np.append(np.zeros(20, dtype=np.int8), np.array(range(20, 20 + i)))
        else:
            train_index = np.zeros(20, dtype=np.int8)
        for trash in range(size_b):
            train_index[:20] = np.random.randint(20, size = 20)
            clf.fit(init_data[train_index, :-1], init_data[train_index,-1])
            ws[trash] = np.around(get_weight(), 2)
        w_std = np.std(ws, axis = 0)
        w = np.mean(ws, axis = 0)
        app = i % 2
        candidate = ""
        npph = np.percentile(w_std, 70)
        nppl = np.percentile(w_std, 33)
        for j in range(len(w)):
            if w_std[j] > npph or w_std[j] < nppl:
                if w[j] > 0:
                    candidate += str(int(app)) + " "
                else:
                    candidate += str(int(not app)) + " "
            else:
                candidate += "0 "
        send(candidate[:-1])
        update = parse_update(receive())
        init_data = np.vstack((init_data, update))
   
    clf.fit(init_data[:, :-1], init_data[:, -1]) 
    w = get_weight()
    candidate = ""
    for i in range(len(w)):
        if w[i] > 0:
            candidate += "1 "
        else:
            candidate += "0 "
    send(candidate[:-1])

   



import socket
import random
import sys
import pdb
import time
import numpy as np
from sklearn.linear_model import SGDRegressor, LinearRegression, BayesianRidge, ARDRegression
from sklearn.linear_model import OrthogonalMatchingPursuit
from sklearn.svm import SVR
from sklearn.cross_validation import Bootstrap


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
#    clf = Perceptron()
#Best so far
#    clf = SGDRegressor(verbose=0, n_iter=20000, power_t=0.01, learning_rate='constant', 
#                       fit_intercept=False, eta0 = 0.01, alpha=0)
        clf = BayesianRidge(fit_intercept=False)
#    clf = ARDRegression(fit_intercept=False)
#    clf = SVR(kernel='linear')
    get_weight = lambda: clf.coef_
    
    if n <= 40:
        size_b = 3000
    else:
        size_b = 3000
    ws = size_b * [0]
    for i in range(19):
#        if i > 0:
#            train_data = np.vstack((train_data[:-1, :], np.append(train_data[-1, :-1], [1]))) 
#        pdb.set_trace()
        if i > 0:
            train_index = np.append(np.zeros(20, dtype=np.int8), np.array(range(20, 20 + i)))
        else:
            train_index = np.zeros(20, dtype=np.int8)
        #This does better than 1, 150 and 2500. Why?
        for trash in range(size_b):
            train_index[:20] = np.random.randint(20, size = 20)
            clf.fit(init_data[train_index, :-1], init_data[train_index,-1])
            ws[trash] = np.around(get_weight(), 2)
#        clf.fit(init_data[:, :-1], init_data[:,-1])
#        clf.fit(update[:, :-1], update[:, -1])
#        pdb.set_trace()
        w_std = np.std(ws, axis = 0)
        w = np.mean(ws, axis = 0)
#        w = get_weight()
#        pdb.set_trace()
        app = i % 2
        candidate = ""
        npph = np.percentile(w_std, 70)
        nppl = np.percentile(w_std, 33)
        for j in range(len(w)):
#            if True:
            if w_std[j] > npph or w_std[j] < nppl:
                if w[j] > 0:
                    candidate += str(int(app)) + " "
                else:
                    candidate += str(int(not app)) + " "
            else:
                candidate += "0 "
            if w[j] >= 1:
                print w
        send(candidate[:-1])
#        zeros = ""
#        for zero in i_zeros(n, i + 4):
#            zeros += str(zero) + " "
#        zeros = zeros[:-1]
#        send(zeros)
        update = np.array(parse_update(receive()))
        #pdb.set_trace()
        init_data = np.vstack((init_data, update))#, np.append((1 - update[:-1]), -update[-1])))
   
#    clf = SGDRegressor(verbose=0, n_iter=20000, power_t = 0.0001)
    clf.fit(init_data[:, :-1], init_data[:, -1]) 
    w = get_weight()
    candidate = ""
    for i in range(len(w)):
        if w[i] > 0:
            candidate += "1 "
        else:
            candidate += "0 "
    send(candidate[:-1])

   



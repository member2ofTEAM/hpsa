import socket
import random
import sys
import pdb
import time
import numpy as np

def send(msg):
    print "sending"
    print "Send: " + msg
    msg += "\n<EOM>\n"
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
    pre_data = n*[0]
    for i in range(n):
        pre_data[i] = rest[i].split(" ")
    return (n, np.array(pre_data))
   
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    send("TEAM")
    pdb.set_trace()
    (n, init_data) = parse_data(receive())
    for i in range(20):
        zeros = ""
        for zero in n * [0]:
            zeros += "0 "
        send(zeros)
        status = receive()
    

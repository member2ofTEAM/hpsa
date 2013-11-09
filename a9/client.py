import socket
import random
import sys
import pdb
import time

def send(msg):
    print "sending"
    print "Send: " + msg
    msg += '<EOM>'
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
    msg = msg[:-5]
    return msg
   
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    pdb.set_trace()
    print receive()
    send("TEAM")
    print receive()
    s.close() 
    s.connect(('127.0.0.1', int(sys.argv[1])))
    send("0 10")
    print receive()

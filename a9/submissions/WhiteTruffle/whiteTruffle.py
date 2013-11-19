import socket
import sys
import time
import random
from auctionGreedy import auctionGreedy

eom = "<EOM>"
maxlen = 999999

def send(msg):
    msg += "\n<EOM>\n"
    print "sending: " + msg
    totalsent = 0
    while totalsent < len(msg):
        sent = s.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
        
def receive():
    print 'receiving some stuff'
    inpData=''
    while True:
        chunk = s.recv(maxlen)
        if not chunk:
            break
        elif chunk == '':
            raise RuntimeError("socket connection broken")
        inpData = inpData + chunk
        if eom in inpData:
            break
    inpData=inpData.strip()[:-len(eom)]
    return inpData.strip()
  
if __name__ == "__main__":
    port = 4567
    if (len(sys.argv) > 1):
        port = int(sys.argv[1])
    print 'port is ' + str(port)
    clientName = 'WhiteTruffle'
    if len(sys.argv) > 2:
        clientName = sys.argv[2]
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    print 'successfully connected'
    print receive()
    s.send(str(clientName))
    #print receive()
    msg = receive()
    #print msg
    a = auctionGreedy(msg)
    while(1):
        bidStr = a.getStrategyStr()
        s.send(bidStr)
        msg = receive()
        if not msg:
            break
        print msg
        a.setAuctionResult(msg)


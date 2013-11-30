import socket, sys
import random
import pdb
from subprocess import Popen, PIPE
import time
import numpy as np
import itertools as it
from exceptions import ZeroDivisionError

teamname="RandomBrie"
port=4567
eom = "<EOM>"
maxlen = 999999
dim=1000
print(sys.argv)
if len(sys.argv)>1:
    port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', port))

def readsocket(sock,timeout=0):
    inpData=''
    while True:
        chunk = sock.recv(maxlen)
        if not chunk: break
        if chunk == '':
            raise RuntimeError("socket connection broken")
        inpData = inpData + chunk
        if eom in inpData:
            break
    inpData=inpData.strip()[:-len(eom)]
    serversaid(inpData.replace('\n', ' [N] ')[:90])
    return inpData.strip()

def sendsocket(sock,msg):
    msg += eom
    totalsent=0
    MSGLEN = len(msg)
    while totalsent < MSGLEN:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    isaid(msg)

def makemove(socket,pid,x,y):
    sendsocket(socket,"(%d,%d,%d)"%(pid,x,y))

def serversaid(msg):
    print("Server: %s"%msg[:80])
def isaid(msg):
    print("Client: %s"%msg[:80])

class State:
    def __init__(self):
        # personal
        self.moves = []
        self.somezip = lambda *x: it.islice(it.izip_longest(*x), len(x[0]))

    def update_state(self, statestr):
        statestr = statestr.split("\n")
        if statestr[1]:
            exec("self.moves = [" + statestr[1] + "]")
            p1moves = []
            p2moves = []
            for move in self.moves:
                if move[0] == 1:
                    p1moves.append(move[1:])
                else:
                    p2moves.append(move[1:])
            self.moves = self.somezip(p1moves, p2moves)
            self.moves = [item for sublist in self.moves for item in sublist if item]


if __name__=="__main__":
    print "Get question from socket"
    # Protocol 2
    question=readsocket(s,1)
    assert (question=='Team Name?')
    sendsocket(s, "Briagonal")
    # Protocol 3, read and parse parameters
    params=readsocket(s)
    params=params.split(',')
    n_pl=int(params[0])
    N=int(params[1])
    assert(int(params[2])==dim)
    pid=int(params[3])
    state=State()

    # Game phase 4
    for turn in xrange(N):
        for pl in range(1,n_pl+1):
            statestr=readsocket(s)
            state.update_state(statestr)
            if pl == pid:
                if turn == N - 1:
                    input_args = []
                    for move in state.moves:
                        if move:
                            for x in move:
                                input_args.append(str(x))
                    pdb.set_trace()
                    out = Popen(["./TEAM"] + input_args, stdout = PIPE)
                    mymove = map(int, out.communicate()[0].split(" "))
                    makemove(s,pid,mymove[0],mymove[1])
                else:
                    #Calculate the id of the other player
                    if state.moves:
                        omove = state.moves[-1]
                    else:
                        omove = (500, 500)
                    mymove = (500-(omove[0] - 500), 500-(omove[1]-500))
                    #Should we select a greedy stone if the move already exists?
                    while (mymove in state.moves):
                        mymove = (max(min(mymove[0] + random.randint(-2, 2), 1000), 0),
                                  max(min(mymove[1] + random.randint(-2, 2), 1000), 0))
                    makemove(s,pid,mymove[0],mymove[1])
    s.close()

import socket, sys
import random
import pdb
import time
import math
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
        self.pl = 1
        self.somezip = lambda *x: it.islice(it.izip_longest(*x), len(x[0]))

    def update_state(self, statestr):
        statestr = statestr.split("\n")
        self.pl = int(statestr[0].split(",")[0].strip())
        if statestr[1]:
            exec("self.moves = [" + statestr[1] + "]")
            #p1moves = []
            #p2moves = []
            moves = []
            for move in self.moves:
                moves.append(move[1:])
            self.moves = moves
            #    if move[0] == 1:
            #        p1moves.append(move[1:])
            #    else:
            #        p2moves.append(move[1:])
            #self.moves = self.somezip(p1moves, p2moves)
            #self.moves = [item for sublist in self.moves for item in sublist if item]


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
    plac = range(N)
    random.shuffle(plac)
    # Game phase 4
    turn = 0
    pl = 1
    while (turn < N):
        statestr=readsocket(s)
        state.update_state(statestr)
        if pl > state.pl:
            turn += 1
        pl = state.pl
        if pl == pid:
            if turn == N - 1 and n_pl == 2:
                input_args = []
                for move in state.moves:
                    if move:
                        for x in move:
                            input_args.append(str(x))
                out = Popen(["./TEAM"] + input_args, stdout = PIPE)
                mymove = map(int, out.communicate()[0].split(" "))
                makemove(s,pid,mymove[0],mymove[1])
            else:
                #Calculate the id of the other player
                if state.moves:
                    #mirror last
                    #choice = random.randint(1, n_pl - 1)
                    #omove = state.moves[-choice]
                    #Cirlce
                    if turn % 2 == 1:
                         omove = (499 + 250 * math.sin(6.28 * float(plac[turn])/N),
                                  499 + 250 * math.cos(6.28 * float(plac[turn])/N))
                    else:
                         omove = (499 + 200 * math.sin(6.28 * float(plac[turn])/N),
                                  499 + 200 * math.cos(6.28 * float(plac[turn])/N))
                    #omove = (np.mean(map(lambda x: x[0], state.moves[-(n_pl - 1):])),
                    #         np.mean(map(lambda x: x[1], state.moves[-(n_pl - 1):])))
                else:
                    omove = (500, 500)
                    #Mirror
                    #mymove = (500-(omove[0] - 500), 500-(omove[1]-500))
                mymove = (int(omove[0]), int(omove[1]))
                #Should we select a greedy stone if the move already exists?
                r = 1
                #pdb.set_trace()
                #while mymove in state.moves:
                    #mymove = (max(min(mymove[0] + random.randint(-r, r), 1000), 0),
                    #          max(min(mymove[1] + random.randint(-r, r), 1000), 0))
                    #r += 1
                makemove(s,pid,mymove[0],mymove[1])
    s.close()

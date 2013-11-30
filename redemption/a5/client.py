import socket, sys
import random
import pdb
import time
import numpy as np
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
    def __init__(self,noplayers,Nstones,playerid):
        # personal
        self.playerid=playerid
        # game parameters
        self.Nstones=Nstones
        self.noplayers=noplayers
        # changing game
        self.nextplayer=0
        self.timeleft=-1.00
        self.moves=[]

    def parsestate(self,statestr):
        state=statestr.split('\n')
        line1=state[0].split(',')
        self.nextplayer=int(line1[0])
        if self.nextplayer==self.playerid:
            self.timeleft=float(line1[1])
        self.parsemoves(state[1])

    def parsemoves(self,movestr):
        self.moves=[[] for i in range(0,self.noplayers+1)]
        if len(movestr)==0: return # no moves yet
        movelist=movestr.split('),(')
        movelist[0]=movelist[0][1:]
        movelist[-1]=movelist[-1][:-1]
        for m in movelist:
            m=m.split(',')
            mid=int(m[0])
            x =int(m[1])
            y =int(m[2])
            self.moves[mid].append((x,y))

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
    state=State(n_pl, N, pid)

    # Game phase 4
    for turn in xrange(N):
        for pl in range(1,n_pl+1):
            statestr=readsocket(s)
            state.parsestate(statestr)
            assert(pl==state.nextplayer)
            if pl == pid:
                #Calculate the id of the other player
                oid = (pid + 1)
                if oid == state.noplayers + 1:
                    oid = 1
                if state.moves[oid]:
                    omove = state.moves[oid][-1]
                else:
                    omove = (500, 500)
                mymove = (500-(omove[0] - 500), 500-(omove[1]-500))
                #Should we select a greedy stone if the move already exists?
                while (mymove in state.moves[oid]):
                    mymove = (max(min(mymove[0] + random.randint(-2, 2), 1000), 0),
                              max(min(mymove[1] + random.randint(-2, 2), 1000), 0))
                makemove(s,pid,mymove[0],mymove[1])
    state.parsestate(readsocket(s))

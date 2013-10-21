
import socket, sys
import time
from exceptions import ZeroDivisionError
from subprocess import Popen, PIPE

teamname="TEAM"
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
#    serversaid(inpData.replace('\n', ' [N] ')[:90])
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
#    isaid(msg)
    
def serversaid(msg):
    print("Server: %s"%msg[:80])
def isaid(msg):
    print("Client: %s"%msg[:80])
def makemove(socket,pid,x,y):
    sendsocket(socket,"(%d,%d,%d)"%(pid,x,y))
def distance_squared(x0, y0, x1, y1):
    return (x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1)

class State:
    def __init__(self):
        # personal
        self.moves=[]

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
            self.moves = zip(p1moves, p2moves)
            self.moves = [item for sublist in self.moves for item in sublist]

if __name__=="__main__":
    # Protocol 2
    question=readsocket(s,1)
    assert (question=='Team Name?')
    sendsocket(s, teamname)

    # Protocol 3, read and parse parameters
    params=readsocket(s)
    params=params.split(',')
    #We assume there are two players
    #We assume we have at most 15 stones to set
    max_stones=int(params[1])
    #Make sure the board dimensions match the standard
    assert(int(params[2])==dim)
    #We are either player 0 or player 1
    our_pid=int(params[3]) - 1
    #We expect there to be at most 2 players
    assert(int(params[3]) in [1, 2])

    state=State()
    # Game phase 4
    for turn in xrange(max_stones):
        #OUR PLAYER CONVENTION IS DIFFERENT FROM THE PROTOCOL
        for pl in range(2):
            state.update_state(readsocket(s))
            if pl == our_pid:
                print "Thinking really hard"
                print state.moves
                f = open("input", "wb")
                for move in state.moves:
                    for x in move:
                        f.write(str(x) + " ")
        		print str(our_pid)
                out = Popen(["./TEAM"], stdout = PIPE)
                move = out.communicate()[0].split(" ")
                print move
                print "Score: " + str(move[2])
                makemove(s, our_pid + 1, int(move[0]), int(move[1]))

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    

import socket
import random
import sys
import pdb
import networkx as nx
import numpy
import pdb

programs = ["dlru", "dlur", "drlu", "drul", "dulr", "durl", "ldru", "ldur", "lrdu", "lrud", "ludr", "lurd", "rdlu", "rdul", "rldu", "rlud", "rudl", "ruld", "udlr", "udrl", "uldr", "ulrd", "urdl", "urld"];
firstNames = ["Jaded", "Jaunty", "Jealous", "Jerky", "Jolly", "Joyful", "Juicy", "Jumpy", "Justifiable", "Juvenile"]
lastNames = ["Jam", "Janitor", "Jelly", "Jerk", "Jet", "Jitterbug", "Journalist", "Judge", "Juice", "Juxtaposition"]

class Muncher():

    def __init__(self, start, program, player):
        self.node = start
        nodes_owner[self.node] = player
        self.program = program
        self.next_move = 0
        self.player = player

    #Return next node (may be same position), -1 if muncher disintegrated
    def next(self):
        if self.node == -1:
            return -1
        next_nodes = map(lambda x: spatial_neighbor_to(self.node, self.program[x]), range(4))
        if len(frozenset(next_nodes)) == 1:
            return -1
        else:
            for i in range(4):
                maybe_next = next_nodes[self.next_move]
                if (maybe_next != -1 and not nodes_owner[maybe_next]):
                    self.node = next_nodes[self.next_move]
                    self.next_move = (self.next_move + 1) % 4
                    return self.node
                self.next_move = (self.next_move + 1) % 4
            return -1

    def get_pos(self):
        return self.node

def send(msg):
    print "sending"
    print msg
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

def parseData(data):
    isNode = False
    isEdge = False
    nodes = []
    edges = []
    edges_data = []
    for line in data.split():
        line = line.strip().lower()
        if 'nodeid,xloc,yloc' in line:
            isNode = True
        elif 'nodeid1' in line:
            isEdge = True
            edges = [dict() for i in xrange(len(nodes))]
        elif isEdge:
            [node1, node2] = map(int, line.split(','))
            edges_data.append([node1, node2])
            if nodes[node1][0] == nodes[node2][0]:
                if nodes[node1][1] > nodes[node2][1]:
                    edges[node1]['u'] = node2
                    edges[node2]['d'] = node1
                else:
                    edges[node1]['d'] = node2
                    edges[node2]['u'] = node1
            else:
                if nodes[node1][0] > nodes[node2][0]:
                    edges[node1]['l'] = node2
                    edges[node2]['r'] = node1
                else:
                    edges[node1]['r'] = node2
                    edges[node2]['l'] = node1
        elif isNode:
            temp = map(int, line.split(','))
            nodes.append((temp[1], temp[2]))
    return (nodes, edges, edges_data)
        
def parseStatus(status):
    munched = set()
    liveMunchers = []
    otherLiveMunchers = []
    lines = status.split()
    if lines[0] != '0':
        [num, munchedNodes] = lines[0].split(':')
        munchedNodes = map(int, munchedNodes.split(','))
        for i in xrange(int(num)):
            munched.add(munchedNodes[i])
    if lines[1] != '0':
        [num, myMunchers] = lines[1].split(':')
        myMunchers = myMunchers.split(',')
        for i in xrange(int(num)):
            temp = myMunchers[i].split('/')
            liveMunchers.append((int(temp[0]), temp[1], int(temp[2])))
    if lines[2] != '0':
        [num, otherMunchers] = lines[2].split(':')
        otherMunchers = map(int, otherMunchers.split(','))
        for i in xrange(int(num)):
            otherLiveMunchers.append(otherMunchers[i])
    scores = map(int, lines[3].split(','))
    remainingStuff = map(int, lines[4].split(','))
    return (munched, liveMunchers, otherLiveMunchers, scores, remainingStuff)

def randomMove(munched):
    rand = random.randint(0, remainingStuff[0])
    nextMove = str(rand)
    if rand == 0:
        return nextMove
    nextMove += ':'
    for i in xrange(rand):
        randNode = random.randint(1, len(nodes)) - 1
        while randNode in munched:
            randNode = random.randint(1, len(nodes)) - 1
        munched.add(randNode)
        nextMove += '{0}/{1},'.format(randNode, programs[random.randint(1, 24) - 1])
    nextMove = nextMove[:-1]
    print "nextMove"
    print nextMove
    return nextMove

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', int(sys.argv[1])))
send(firstNames[random.randint(1, len(firstNames)) - 1] + lastNames[random.randint(1, len(lastNames)) - 1])
(nodes, edges, edges_data) = parseData(receive())
pdb.set_trace()
G = nx.Graph()
G.add_edges_from(edges_data)
NO_NODES = len(nodes)
NO_EDGES = len(edges_data)
round = 0
munched = set()
while(True):
    status = receive()
    print status
    if status == '0' or status == '':
        break
    (newlyMunched, liveMunchers, otherLiveMunchers, scores, remainingStuff) = parseStatus(status)
    munched.update(newlyMunched)
    print len(newlyMunched), len(liveMunchers), len(otherLiveMunchers), scores, remainingStuff
    send(randomMove(munched))
    round += 1


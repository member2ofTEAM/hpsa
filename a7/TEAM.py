import socket
import random
import sys
import pdb
import networkx as nx
import numpy
import pdb

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
    for line in data.split():
        line = line.strip().lower()
        if 'nodeid,xloc,yloc' in line:
            isNode = True
        elif 'nodeid1' in line:
            isEdge = True
        elif isEdge:
            edges.append(map(int, line.split(',')))
        elif isNode:
            nodes.append(map(int, line.split(','))[1:])
    return (nodes, edges)

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

def next_move():
    if len(our_nodes) == 0:
        send('2:1/urld,2/urld')
        our_nodes.append(1)
        our_nodes.append(2)
    else:
        send('0') 

#TODO: Implement the who came first rules etc
def next_round():
    status = receive()
    print status
    if status == '0' or status == '':
        sys.exit(0)
    (newlyMunched, liveMunchers, otherLiveMunchers, scores, remainingStuff) = parseStatus(status)
    for m in liveMunchers:
        our_nodes.append(m[0])
    for node in newlyMunched:
        nodes_owner[node] = 2
    for node in our_nodes:
        nodes_owner[node] = 1
    print len(newlyMunched), len(liveMunchers), len(otherLiveMunchers), scores, remainingStuff
    next_move()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', int(sys.argv[1])))
send("TEAM")

munchers = [(1, 'urld'), (2, 'urld')]

G = nx.Graph()
(nodes_data, edges_data) = parseData(receive())
G.add_edges_from(edges_data)
NO_MUNCH = 10
NO_NODES = len(nodes_data)
NO_EDGES = len(edges_data)
round = 0

#0 means neutral, 1 means player 1, 2 means player 2
nodes_owner = NO_NODES * [0]
our_nodes = []

while(1):
    next_round()

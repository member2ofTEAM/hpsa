import socket
import random
import sys
import pdb
import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy
import pdb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Tkinter as Tk

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
        if len(frozenset(next_nodes)) != 1:
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

    def __str__(self):
        return str(self.node) + "/" + str(self.program)

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

def spatial_neighbor_to(node, direction):
    node_pos = nodes_data[node]
    moves = {"l":(-1, 0), "r":(1, 0), "u":(0,1), "d":(0,-1)}
    offset = moves[direction]
    maybe_nb = [node_pos[0] + offset[0], node_pos[1] + offset[1]]
    try:
        maybe_nb = nodes_data.index(maybe_nb)
        if ([node, maybe_nb] in edges_data or [maybe_nb, node] in edges_data): 
            return maybe_nb
        return -1
    except ValueError:
        return -1

def redraw():
    a.cla()
    colors = [nodes_owner[node] for node in G.nodes()]
    plt.xlim(-1, 20)
    plt.ylim(-1, 10)
    a.set_xticks(numpy.arange(-1, 20, 1))
    a.set_yticks(numpy.arange(-1, 10, 1))
    plt.grid(which='both')
    nx.draw_networkx(G, nodes_data, cmap = plt.get_cmap('jet'), 
                        node_color = colors, font_color='white')
    canvas.draw()

#TODO: Implement the who came first rules etc
def next_round():
    pdb.set_trace()
    status = receive()
    print status
    if status == '0' or status == '':
        sys.exit(0)
    (newlyMunched, liveMunchers, otherLiveMunchers, scores, remainingStuff) = parseStatus(status)
    for m in liveMunchers.split(":")[1].split(","):
        nodes_owner[m.split("/")[0]) = 1
    for opp_node in otherLiveMunchers:
        nodes_owner[opp_node] = 2
    munched.update(newlyMunched)
    print len(newlyMunched), len(liveMunchers), len(otherLiveMunchers), scores, remainingStuff
    nodes_owner[1] = 1
    nodes_owner[2] = 1
    if round == 0:
        send('1:1/urld,2/urld')
    round += 1
    redraw()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', int(sys.argv[1])))
send("TEAM")

G = nx.Graph()
(nodes_data, edges_data) = parseData(receive())
G.add_edges_from(edges_data)
NO_MUNCH = 10
NO_NODES = len(nodes_data)
NO_EDGES = len(edges_data)
round = 0

#0 means neutral, 1 means player 1, 2 means player 2
nodes_owner = NO_NODES * [0]

root = Tk.Tk()
fig = plt.figure()
a = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

munched = set()

b = Tk.Button(root, text="next round", command=next_round)
b.pack()

Tk.mainloop()



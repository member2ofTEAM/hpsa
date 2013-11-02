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



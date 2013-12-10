import socket
import random
import sys
import pdb
import networkx as nx
import time
import re
from itertools import combinations
from copy import deepcopy

def send(msg):
    print "sending"
    print "Send: " + msg
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
    #pdb.set_trace()
    munched = set()
    liveMunchers = []
    otherLiveMunchers = []
    otherNewMunchers = []
    lines = status.split()
    if lines[0] != '0':
        [num, munchedNodes] = lines[0].split(':')
        munchedNodes = map(int, re.split("[/,]", munchedNodes))
        for i in xrange(int(num)):
            munched.add(munchedNodes[i])
        for m in lines[0].split(':')[1].split(","):
            if "/" in m:
                otherNewMunchers.append(map(int, m.split("/")))
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
    return (munched, liveMunchers, otherLiveMunchers, otherNewMunchers, scores, remainingStuff)

def greedyMove(munched,nodes,edges, edges_data, otherLiveMunchers, round_no, subGs, G, ol):
    move_string = str(0)
    subGs.sort(key = lambda x: len(x), reverse=True)
    #pdb.set_trace()
    points = []
    maxy = 0
    chosen = 0
    #consider contains a list of munchers we can answer the enemy with
    consider = [m for m in otherLiveMunchers] #m[1] for m in ...
    for enemy in consider:
        for node in edges[enemy].values():
            if node in subGs[0].nodes() and node not in consider:
                points.append(node)
                break
    for node in subGs[0].nodes():
        if maxy > nodes[node][1]:
            maxy = nodes[node][1]
            chosen = node
    if ol and not otherLiveMunchers:#not otherNewMunchers:
    	points = [chosen]
    move_string = str(len(points)) + ':'
    for point in points:
        move_string += str(point) + "/ulur,"
    move_string = move_string[:-1]
    return move_string

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    send("TEAM")
    (nodes, edges, edges_data) = parseData(receive())
    nodes_owner = [0] * len(nodes)
    G = nx.Graph()
    G.add_edges_from(edges_data)
    round_no = 0
    munched = set()
    ol = 0
    while(True):
        status = receive()
        if not status:
	    continue
        print "Status: " + status
        if round_no > 1000:
            break
        (newlyMunched, liveMunchers, otherLiveMunchers, 
            otherNewMunchers, scores, remainingStuff) = parseStatus(status)
        munched.update(newlyMunched)
        G.remove_nodes_from(munched)
        subGs = nx.connected_component_subgraphs(G)
        if len(otherLiveMunchers):
	    ol = 1
        send(greedyMove(munched, nodes, edges, edges_data,
                            otherLiveMunchers, round_no, subGs, G, ol))
        round_no += 1
    print remainingStuff[2]


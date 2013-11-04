import socket
import random
import sys
import pdb
#import networkx as nx
import time
import re

programs = ["dlru", "dlur", "drlu", "drul", "dulr", "durl", "ldru", "ldur", "lrdu", "lrud", "ludr", "lurd", "rdlu", "rdul", "rldu", "rlud", "rudl", "ruld", "udlr", "udrl", "uldr", "ulrd", "urdl", "urld"];
firstNames = ["Jaded", "Jaunty", "Jealous", "Jerky", "Jolly", "Joyful", "Juicy", "Jumpy", "Justifiable", "Juvenile"]
lastNames = ["Jam", "Janitor", "Jelly", "Jerk", "Jet", "Jitterbug", "Journalist", "Judge", "Juice", "Juxtaposition"]

class Muncher():

    def __init__(self, start, nodes, edges_data, munched, program=None, player=1):
        self.node = start
        self.score = 1
        self.player = player
        self.eaten = [self.node]
        self.program = ""
        if program == None:
            self.program = self._infer_program(nodes, edges_data)
        elif program == "best":
            (self.score, self.program) = self._best_program_by_score(nodes, edges_data, munched)
        else:
            self.program = program

    def _infer_program(self):
        return "urld"

    #Return next node (may be same position), -1 if muncher disintegrated
    def next(self, munched, nodes, edges_data):
        if self.node == -1:
            return -1
        next_nodes = map(lambda x: spatial_neighbor_to(self.node, self.program[x], nodes, edges_data), range(4))
        for i in range(len(next_nodes)):
            maybe_next = next_nodes[i]
            if (maybe_next != -1 and maybe_next not in munched and maybe_next not in self.eaten):
                self.node = maybe_next
                self.score += 1
                self.eaten.append(self.node)
                return self.node
        return -1

    def get_pos(self):
        return self.node

    #Return program with maximum score and score
    def _best_program_by_score(self, nodes, edges_data, munched):
        best_score = -1
        best_program = ''
        for program in programs:
            #The proper way of doing this is to create a copy of self
            score_copy = self.score
            node_copy = self.node
            eaten_copy = self.eaten[:]
            program_copy = self.program

            self.program = program
            #PLAY GAME
            while (self.next(munched, nodes, edges_data) != -1):
                pass

            if self.score > best_score:
                best_score = self.score
                best_program = program
            #Restore changed variables
            self.score = score_copy
            self.node = node_copy
            self.eaten = eaten_copy[:]
            self.program = program_copy

        return (best_score, best_program)

#Return -1 if there is no node in that spatial direction
def spatial_neighbor_to(node, direction, nodes, edges_data):
    node_pos = nodes[node]
    moves = {"l":(-1, 0), "r":(1, 0), "u":(0,-1), "d":(0,1)}
    offset = moves[direction]
    maybe_nb = (node_pos[0] + offset[0], node_pos[1] + offset[1])
    tmp = -1
    for i in range(len(nodes)):
        if nodes[i] == maybe_nb:
            tmp = i	
            break
    maybe_nb = tmp
    if maybe_nb != -1 and ([node, maybe_nb] in edges_data or [maybe_nb, node] in edges_data):
            return maybe_nb
    return -1

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

#Return best (node, program, score) for nodes of interest sorted and maximized by score
def greedy_next(munched, nodes, edges_data, otherNewMunchers):
    nodes_of_interest = []

    for node in otherNewMunchers:
        node = node[1]
        program = "urld"
        neighborhood = map(lambda x: spatial_neighbor_to(node, program[x], nodes, edges_data), range(4))
        for neighbor in neighborhood:
            if not (neighbor in munched) and neighbor != 1:
                nodes_of_interest.append(neighbor)

    ranking = []
    for node in nodes_of_interest:
        m = Muncher(node, nodes, edges_data, munched, "best")
        ranking.append((node, m.program, m.score))

    ranking.sort(key=lambda x: x[2], reverse=True)
    return ranking

def greedyMove(munched,nodes,edges,otherNewMunchers):
    move_string = str(0)
    node = 0
    program = ''
    if remainingStuff[0]>0:
        ranking = greedy_next(munched, nodes, edges_data, otherNewMunchers)
        next_move = ranking[0]
        move_string = '1:'
        move_string += str(next_move[0]) + "/" + str(next_move[1])
    return move_string

#def update_owner(newly_munched, live_munchers, other_live_munchers, nodes_owner):
#    pass
    
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    send(firstNames[random.randint(1, len(firstNames)) - 1] + lastNames[random.randint(1, len(lastNames)) - 1])
    (nodes, edges, edges_data) = parseData(receive())
#    nodes_owner = [0] * len(nodes)
#    G = nx.Graph()
#    G.add_edges_from(edges_data)
    round = 0
    munched = set()
    while(True):
        status = receive()
        print "Status: " + status
        #TODO If the server sends a status that corresponds to nothing, the while loop will break here
        if status == "0" or status == '':
            break
        (newlyMunched, liveMunchers, otherLiveMunchers, 
            otherNewMunchers, scores, remainingStuff) = parseStatus(status)
#        pdb.set_trace()
#        update_owner(newlyMunched, liveMunchers, otherLiveMunchers, nodes_owner)
        munched.update(newlyMunched)
        if otherNewMunchers:
            send(greedyMove(munched,nodes,edges, otherNewMunchers))
        else:
            send("0")
        round += 1


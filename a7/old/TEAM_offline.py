import csv
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import numpy
import pdb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Tkinter as Tk

NO_NODES = 127
NO_EDGES = 131
NO_MUNCH = 10
FILENAME = "nanodata.csv"
input_data = [map(int, i) for i in csv.reader(open(FILENAME)) if i != [] and i[0].isdigit()]
nodes_data = input_data[:NO_NODES]
nodes_data = dict((i[0], (i[1], i[2])) for i in nodes_data)
edges_data = input_data[NO_NODES:NO_NODES + NO_EDGES]
#0 means neutral, 1 means player 1, 2 means player 2
nodes_owner = {}
for node in nodes_data.keys():
    nodes_owner[node] = 0

G = nx.Graph()
G.add_edges_from(edges_data)

root = Tk.Tk()
fig = plt.figure()
a = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

#Return -1 if there is no node in that spatial direction
def spatial_neighbor_to(node, direction):
    node_pos = nodes_data[node]
    moves = {"l":(-1, 0), "r":(1, 0), "u":(0,1), "d":(0,-1)}
    offset = moves[direction]
    maybe_nb = (node_pos[0] + offset[0], node_pos[1] + offset[1])
    inverse_nodes = dict((v, k) for k, v in nodes_data.iteritems())
    maybe_nb = inverse_nodes.get(maybe_nb, -1)
    if maybe_nb == -1:
        return -1
    else:
        if [node, maybe_nb] in edges_data or [maybe_nb, node] in edges_data:
            return maybe_nb
        else:
            return -1

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

muncher = []
muncher.append(Muncher(6, "ruld", 1))
muncher.append(Muncher(10, "ruld", 1))
muncher.append(Muncher(11, "ruld", 2))
muncher.append(Muncher(12, "ruld", 2))

def redraw():
    a.cla()
    colors = [nodes_owner.get(node) for node in G.nodes()]
    plt.xlim(-1, 20)
    plt.ylim(-1, 10)
    a.set_xticks(numpy.arange(-1, 20, 1))
    a.set_yticks(numpy.arange(-1, 10, 1))
    plt.grid(which='both')
    nx.draw_networkx(G, nodes_data, cmap = plt.get_cmap('jet'), node_color = colors, font_color='white')
    canvas.draw()

#TODO: Implement the who came first rules etc
def next_round():
    for m in muncher:
        node = m.next()
        print node
        if node != -1:
            nodes_owner[node] = m.player
    redraw()

b = Tk.Button(root, text="next move", command=next_round)
b.pack()

Tk.mainloop()

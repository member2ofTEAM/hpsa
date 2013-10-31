import csv
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Tkinter as Tk

NO_NODES = 127
NO_EDGES = 131
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

def next_round():
    nodes_owner[1] = 2
    redraw()

b = Tk.Button(root, text="next move", command=next_round)
b.pack()

Tk.mainloop()


import numpy as np
import networkx as nx
import time

from numpy import genfromtxt
from scipy.spatial.distance import cdist

start = time.time()
my_data = genfromtxt('travelingtest', delimiter=' ', usecols = (1,2,3)) #read in data from csv file 
Y = cdist(my_data,my_data, 'euclidean') #create distance matrix
G = nx.Graph(np.matrix(Y))
T = nx.minimum_spanning_tree(G)

d = T.degree()
for node in G.nodes():
	if not node in d.keys():
		G.remove_node(node)
for edge in G.edges():
	G[edge[0]][edge[1]]['weight'] = int(100 - round(0.0023 * G[edge[0]][edge[1]]['weight']))
M = G.subgraph(d.keys())
a = nx.max_weight_matching(M)

H = nx.MultiGraph()
H.add_nodes_from(T.nodes())
H.add_edges_from(T.edges())
for (key, value) in a.items():
	if key < value:
		H.add_edge(key, value)

t = []
for (i, j) in nx.eulerian_circuit(H):
	if i in t:
		continue
	t.append(i)

print time.time() - start
	
#the result is t
t_e = zip(t[:-1], t[1:])
distance = 0
for (i, j) in t_e:
	distance += Y[i, j]
	




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


#WHY DOES THE FOLLOWING NOT WORK?
#WHY IS IT NOT EQUIVALENT TO THE CORRECT VERSION?

d = T.degree() #Get dictionary of node:degree
N = []
for key in d:
	if d[key] % 2 == 1:
		N.append(key)
for i in N:
	for j in N:
		if i != j:
			G[i][j]['weight'] = int(100 - round(0.0023 * G[i][j]['weight']))
M = G.subgraph(N)
# M = nx.adjacency_matrix(M)
# M = 0.0023 * M
# M = M.round()
# a = nx.Graph(100 - M)
a = nx.max_weight_matching(M)


H = nx.MultiGraph()
H.add_nodes_from(T.nodes())
H.add_edges_from(T.edges())
for (key, value) in a.items():
	if key < value:
		H.add_edge(key, value)

t = []
seen = set()
for (i, j) in nx.eulerian_circuit(H):
	if i in seen:
		continue
	seen.add(i)
	t.append(i)

print time.time() - start
	
#the result is t
t_e = zip(t[:-1], t[1:])
distance = 0
for (i, j) in t_e:
	distance += Y[i, j]
	




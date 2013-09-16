import numpy as np
import time
import imp

from numpy import genfromtxt

nx  = imp.load_source('networkx', '/usr/lib/python2.6/site-packages/networkx')

start = time.time()
my_data = genfromtxt('travelingtest', delimiter=' ', usecols = (1,2,3)) #read in data from csv file 
Y = np.zeros(1000000).reshape((1000, 1000))
for i in range(1000):
	for j in range(1000):
		Y[i][j] = np.linalg.norm(my_data[i] - my_data[j])

G = nx.Graph(np.matrix(Y))
T = nx.minimum_spanning_tree(G)

#THIS CAN STILL BE OPTIMIZED
d = T.degree() #Get dictionary of node:degree
N = []
for key in d:
	if d[key] % 2 == 1:
		N.append(key)
M = G.subgraph(N)
M = nx.adjacency_matrix(M)
M = 0.0023 * M
M = M.round()
a = nx.Graph(100 - M)
a = nx.max_weight_matching(a)
#UNTIL HERE

H = nx.MultiGraph()
H.add_nodes_from(T.nodes())
H.add_edges_from(T.edges())
for (key, value) in a.items():
	if N[key] < N[value]:
		H.add_edge(N[key], N[value])

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
	




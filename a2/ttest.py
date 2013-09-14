import numpy as np
import networkx as nx

from numpy import genfromtxt
from scipy.spatial.distance import cdist

my_data = genfromtxt('travelingtest', delimiter=' ', usecols = (1,2,3)) #read in data from csv file 
Y = cdist(my_data,my_data, 'euclidean') #create distance matrix
m = np.matrix(Y)
G = nx.Graph(m)
T = nx.minimum_spanning_tree(G)
d = T.degree() #Get dictionary of node:degree
N = []
for key in d:
	if d[key] % 2 == 1:
		N.append(key)
#Find nodes N with odd degree
M = G.subgraph(N).to_undirected()
a = nx.Graph(-1* nx.adjacency_matrix(M)).to_undirected()
a = nx.max_weight_matching(a, maxcardinality=True)

ae = []
an = M.nodes()
for (key, value) in a.items():
	ae.append((an[key], an[value]))
	
aee = []
for i in ae:
	if i[0] < i[1]:
		aee.append(i)

#a = np.array(A).tolist()
# m = Munkres()
##Compute edges of min cost perfect matching on subset of G
# M = m.compute(A)

H = nx.MultiGraph()
H.add_nodes_from(T.nodes())
H.add_edges_from(T.edges())
H.add_edges_from(aee)
print nx.is_eulerian(H)
E = list(nx.eulerian_circuit(H))

tsp = [i for (i, j) in E]
t = []
seen = set()
for i in tsp:
	if i in seen:
		continue
	seen.add(i)
	t.append(i)
	
#the result is t
t_e = zip(t[:-1], t[1:])
distance = 0
for (i, j) in t_e:
	distance += Y[i, j]
	
stupid_dist = 0
for i in range(0, 999):
	stupid_dist += Y[i][i+1]





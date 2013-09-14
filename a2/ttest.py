import numpy as np
import networkx as nx
from munkres import Munkres	

from numpy import genfromtxt
from scipy.spatial.distance import cdist

my_data = genfromtxt('C:\\Users\\User\\Desktop\\travelingtest.txt', delimiter=' ', usecols = (1,2,3)) #read in data from csv file 
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
M = G.subgraph(N)
A = nx.adjacency_matrix(M)
a = np.array(A).tolist()

m = Munkres()
#Compute edges of min cost perfect matching on subset of G
M = m.compute(A)

H = nx.MultiGraph()
H.add_node(T)
H.add_edges_from(T.edges())
H.add_edges_from(M)
#nx.is_eulerian(H) == false		WTF
#E = nx.eulerian_circuit(H)
#Do shortcutting on E





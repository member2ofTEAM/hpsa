import numpy as np
import networkx as nx
import time
import subprocess

from numpy import genfromtxt
from scipy.spatial.distance import cdist

start = time.time()
my_data = genfromtxt('travelingtest', delimiter=' ', usecols = (1,2,3)) #read in data from csv file 
Y = cdist(my_data,my_data, 'euclidean') #create distance matrix
G = nx.Graph(np.matrix(Y))
T = nx.minimum_spanning_tree(G)

#MINMAXMATCHING
d = T.degree() #Get dictionary of node:degree
N = []
for key in d:
	if d[key] % 2 == 1:
		N.append(key)
f = open("data.dat", "wb")
f.write(str(len(N)))
f.write("\n")
for n in N:
	f.write(str(round(my_data[n][0])) + " ")
	f.write(str(round(my_data[n][1])) + " ")
	f.write(str(round(my_data[n][2])))
	f.write("\n")
f.close()

print "done writing"

fh = open("NUL","w")
subprocess.call(["./blossom4","-3", "-x","data.dat", "-w", "output.dat"], stdout=fh)
fh.close()

print "done pipiing"

result = genfromtxt('output.dat', delimiter=' ', usecols = (0, 1))
result = result[1:]
#MINMAXMATCHING END

H = nx.MultiGraph()
H.add_nodes_from(T.nodes())
H.add_edges_from(T.edges())
for (key, value) in a.items():
	if N < N:
		H.add_edge(N, N)

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
	




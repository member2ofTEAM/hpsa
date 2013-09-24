from numpy import matrix
from numpy import genfromtxt
from sets import Set
from networkx import Graph
from networkx import minimum_spanning_tree
from networkx import MultiGraph
from networkx import eulerian_circuit
from subprocess import call
import sys
from scipy.spatial.distance import cdist

my_data = genfromtxt('input.dat', delimiter=' ', usecols = (1,2,3)) #read in data from csv file 
Y = cdist(my_data,my_data, 'euclidean') #create distance matrix
G = Graph(matrix(Y))
T = minimum_spanning_tree(G)

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

fh = open("trash.dat","w")
call(["./blossom4","-3", "-x","data.dat", "-w", "output.dat"], stdout=fh)
fh.close()

result = genfromtxt('output.dat', delimiter=' ', usecols = (0, 1))
result = result[1:]
#MINMAXMATCHING END

H = MultiGraph()
H.add_nodes_from(T.nodes())
H.add_edges_from(T.edges())
for (key, value) in result:
	H.add_edge(N[int(key)], N[int(value)])

f = open("data.dat", "wb")
t = Set()
for (i, j) in eulerian_circuit(H):
	if i in t:
		continue
	t.add(i)
	f.write(str(i) + " ")
f.close()

fh = open("trash.dat", "w")
call(["./exe", 'input.dat'], stdout = fh)
fh.close()

#the result is t
f = open("result.dat", "rb")
s = f.read()
f.close()
s = s.replace(";", "")
s = s.split(" ")[:-1]
print s
for i in range(1000):
        s[i] = int(s[i]) - 1
t_e = zip(s[:-1], s[1:])
distance = 0
for (i, j) in t_e:
        distance += Y[i, j]
print distance


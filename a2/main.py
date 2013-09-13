from numpy import genfromtxt
from scipy.sparse import csr_matrix
from scipy.spatial.distance import cdist
from scipy.sparse.csgraph import minimum_spanning_tree

my_data = genfromtxt('C:\\Users\\Sven\\Desktop\\travelingtest.csv', delimiter=' ', usecols = (1,2,3)) #read in data from csv file 

Y = cdist(my_data,my_data, 'euclidean') #create distance matrix

X = csr_matrix(Y)
Tcsr = minimum_spanning_tree(X) #calculate minimum spanning tree
#Tcsr.toarray().astype(int)



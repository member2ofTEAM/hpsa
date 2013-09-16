import itertools

from numpy import genfromtxt
from scipy.sparse import csr_matrix
from scipy.spatial.distance import cdist
from scipy.sparse.csgraph import minimum_spanning_tree


def find_best_among_10(ten, d):
        best = (float("inf"), ten)
        for i in itertools.permutations(ten, 10):
                pairs = zip(i[:-1], i[1:])
                length = 0
                for p in pairs:
                        length += d[p[0]][p[1]]
                if length < best[0]:
                        best = (length, i)
        return best[1]


if __name__ == "__main__":
	my_data = genfromtxt('travelingtest', delimiter=' ', usecols = (1,2,3))
	d = cdist(my_data,my_data, 'euclidean') #create distance matrix
	#X = csr_matrix(Y)
	#Tcsr = minimum_spanning_tree(X) #calculate minimum spanning tree
	#Tcsr.tarray().astype(int)
	ten = [x - 1 for x in range(0, 101, 10)][1:]
	print find_best_among_10(ten, d)

		

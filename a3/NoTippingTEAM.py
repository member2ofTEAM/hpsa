'''
Created on 25.09.2013

@author: Sven, Christian, Collin

Communicates with the Server
'''
from Game_optimized_12 import NoTipping
import sys

A = NoTipping()
A.get_input(int(sys.argv[1]),int(sys.argv[2]))
move = A.magic_alphabeta_search()
A.make_move(move)
print str(move[0]) + " " + str(move[1])
A.display()
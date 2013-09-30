'''
Created on 25.09.2013

@author: Sven, Christian, Collin

Just a small test utility to initialize a game and make some moves
'''
from Game_optimized_12 import NoTipping
from Game_optimized_12 import alphabeta_search
import random
import pdb
import sys

A = NoTipping()
#A.get_input(int(sys.argv[1]),int(sys.argv[2]))
A.display()
#c = alphabeta_full_search(b,A)
#print c
'''
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
'''

print A.to_move
print A.phase


#pdb.set_trace()
while True:
    if A.to_move == 1:
        pdb.set_trace()
        move = A.magic_alphabeta_search()
        A = A.make_move(move)
        A.display()
        if A.board.tipped():
            break
    else:
        move = A.magic_alphabeta_search()
        A = A.make_move(move)
        A.display()
        if A.board.tipped():
            break

if(A.to_move==1):
    print "Player "+str(A.to_move)+" wins"
else:
    print "Player "+str(A.to_move)+" wins"

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
#        pos = int(raw_input("Enter Position: "))
#        wei = int(raw_input("Enter Weight: "))
        #((pos, wei), score) = alphabeta_search(A, d=1)
        #move = (pos,wei)
        move = A.magic_alphabeta_search()
        A = A.make_move(move)
        A.display()
        if A.board.tipped():
            break
    else:
#        if A.board.tipped():
#            break
#        ((pos, wei), score) = alphabeta_search(A, d=1)
        #((pos, wei), score) = alphabeta_search(A, d=1)
        #move = (pos,wei)
        move = A.magic_alphabeta_search()
        A = A.make_move(move)
        A.display()
        if A.board.tipped():
            break
        #pos = int(raw_input("Enter Position: "))
        #wei = int(raw_input("Enter Weight: "))
        #move = (pos, wei)
        #A = A.make_move(move)
        #A.display()
        
        
#        random.random()
#        move = random.choice(A.valid_moves[A.to_move])
#        A = A.make_move(move)
#        A.display()
        
        
#        if A.board.tipped():
#            break

if(A.to_move==1):
    print "Player "+str(A.to_move)+" wins"
else:
    print "Player "+str(A.to_move)+" wins"

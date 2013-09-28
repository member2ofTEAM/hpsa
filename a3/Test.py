'''
Created on 25.09.2013

@author: Sven

Just a small test utility to initialize a game and make some moves
'''
from Game_clean import NoTipping
from Game_clean import alphabeta_search
import random
import pdb

A = NoTipping()
A.display()

#c = alphabeta_full_search(b,A)
#print c


pdb.set_trace()
while True:
    if A.to_move == 1:
#        pos = int(raw_input("Enter Position: "))
#        wei = int(raw_input("Enter Weight: "))
        ((pos, wei), score) = alphabeta_search(A, d=1)
        move = (pos,wei)
        A = A.make_move(move)
        A.display()
        if A.board.tipped():
            break
    else:
        if A.board.tipped():
            break
#        ((pos, wei), score) = alphabeta_search(A, d=1)
        pos = int(raw_input("Enter Position: "))
        wei = int(raw_input("Enter Weight: "))
        move = (pos, wei)
        A = A.make_move(move)
        A.display()
        
        
#        random.random()
#        move = random.choice(A.valid_moves[A.to_move])
#        A = A.make_move(move)
#        A.display()
        
        
        if A.board.tipped():
            break

if(A.to_move==1):
    print "Player wins"
else:
    print "Computer wins"

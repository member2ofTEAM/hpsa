'''
Created on 25.09.2013

@author: Sven

Just a small test utility to initialize a game and make some moves
'''
from Game import *

A = NoTipping()
A.display()
b = A.initial

#c = alphabeta_full_search(b,A)
#print c


while True:
    if b.to_move == 1:
        pos = int(raw_input("Enter Position: "))
        wei = b.to_move * int(raw_input("Enter Weight: "))
        move = (pos,wei)
        b = A.make_move(move, b, A.board)
        A.display()
        
        if A.board._tipped():
            break
    else:    
        if A.board._tipped():
            break
        random.random()
        move = random.choice(b.moves[b.to_move])
        b = A.make_move(move, b, A.board)
        A.display()
        
        
        if A.board._tipped():
            break

if(b.to_move==1):
    print "Player wins"
else:
    print "Computer wins"

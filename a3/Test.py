'''
Created on 25.09.2013

@author: Sven, Christian, Collin

Just a small test utility to initialize a game and make some moves
'''
from TEAMengine import NoTipping
import pdb
import sys

A = NoTipping()
A.display()

print A.to_move
print A.phase

#pdb.set_trace()
while True:
    if A.to_move == 1:

        move = A.magic_alphabeta_search()
#        x = raw_input()
#        y = x.split(" ")
#        move = (int(y[0]), int(y[1]))
        A = A.make_move(move)

        A.display()
        if A.board.tipped():
            break
    else:

        move = A.magic_alphabeta_search()
#        x = raw_input()
#        y = x.split(" ")
#        move = (int(y[0]), int(y[1]))
        A = A.make_move(move)

        A.display()
        if A.board.tipped():
            break

if(A.to_move==1):
    print "Player "+str(A.to_move)+" wins"
else:
    print "Player "+str(A.to_move)+" wins"

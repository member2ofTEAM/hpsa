import subprocess as sp
from subprocess import check_output as checkout
import numpy as np
import sys
import time

def calc_torque(board_info,grav_center,support):
    board = np.vstack((board_info,grav_center))
    torque = 0
    for e in board:
        torque = torque + (e[0] - support) * e[1]
    return torque

def player_move(player_arg,mode,player,player_time):
    time_remain = 120 - player_time
    args = (player_arg + ' ' + str(mode) + ' ' + str(player) + ' ' + 
           str(time_remain))
    output = checkout(args,shell = True)
    output = output.split()
    move = [int(output[0]),int(output[1]),player]
    return move

def adding_verify(move,pwt,bd):
    v = True
    # check position
    if move[0] not in bd:
        v = False
    # check wt
    if move[1] not in pwt:
        v = False
    return v

def tipping(board_info,grav_center,support1,support2):
    tip = False
    torque1 = calc_torque(board_info,grav_center,support1)
    torque2 = calc_torque(board_info,grav_center,support2)
    if torque1 < 0 and torque2 < 0:
        tip = True
    if torque1 > 0 and torque2 > 0:
        tip = True
    return torque1,torque2,tip

def removing_verify(move,board_info,player,player1,player2):
    v = True
    # no such wt on board
    if board_info[move[0]+15][1] != move[1]:
        v = False
    # player1 cannot move wt placed by player2 unless no other wts left
    if player == player1:
        if board_info[move[0]+15][2] == player2:
            if player1 in board_info[:,2]:
                v = False
    return v

def output(board_info,record,move,torque1,torque2):
    np.savetxt('board.txt',board_info,fmt='%d')
    record.write(str(mode)+ ' ' + str(move[0]) + ' ' + str(move[1])
                 + ' ' + str(move[2]) + ' ' +str(int(torque1)) + ' ' +
                 str(int(torque2)) + '\n')

#-----------------------
player_file = open('run.txt','r')
player1_arg = player_file.readline().rstrip('\n')
player2_arg = player_file.readline().rstrip('\n')
player1 = 1
player2 = 2
player1_time = 0
player2_time = 0
record = open('move.txt','w')
support1 = -3
support2 = -1
grav_center = np.array([0,3,0])

# set board
init_board = np.zeros((31,3))
init_board[:,0] = range(-15,16)
 # 3kg at -4
init_board[-4 + 15][1] = 3
np.savetxt('board.txt',init_board,fmt='%d')

# mode = 1: adding mode. mode = 2: removing mode. 
mode = 1
step = 0
p1wt = range(1,13)
p2wt = range(1,13)
bd = range(-15,16)
bd.remove(-4)
winner = 0

# adding mode
while step < 24:
 # player 1
    board_info = np.loadtxt('board.txt')
    start = time.time()
    move = player_move(player1_arg,mode,player1,player1_time)
    end = time.time()
    player1_time = player1_time + end - start
    if player1_time > 120:
        winner = player2
        break
    # accept move?
    if not adding_verify(move,p1wt,bd):
        winner = player2
        print 'Invalid move: ' + str(move)
        break
    # update board
    board_info[move[0] + 15] = move
    # tip?
    torque1,torque2,check_tip = tipping(board_info,grav_center,support1
                                        ,support2)
    if check_tip:
        winner = player2
        output(board_info,record,move,torque1,torque2)
        break
    output(board_info,record,move,torque1,torque2)
    bd.remove(move[0])
    p1wt.remove(move[1])
    step = step + 1

 # player 2
    board_info = np.loadtxt('board.txt')
    start = time.time()
    move = player_move(player2_arg,mode,player2,player2_time)
    end = time.time()
    player2_time = player2_time + end - start
    if player2_time > 120:
        winner = player1
        break
    # accept move?
    if not adding_verify(move,p2wt,bd):
        winner = player1
        print 'Invalid move: ' + str(move)
        break
    # update board
    board_info[move[0] + 15] = move
    # tip?
    torque1,torque2,check_tip = tipping(board_info,grav_center,support1
                                        ,support2)
    if check_tip:
        winner = player1
        output(board_info,record,move,torque1,torque2)
        break
    output(board_info,record,move,torque1,torque2)
    bd.remove(move[0])
    p2wt.remove(move[1])
    step = step + 1

if winner == 0:
# removing mode
    mode = 2
    while step <= 49:

     # player 1
        board_info = np.loadtxt('board.txt')
        start = time.time()
        move = player_move(player1_arg,mode,player1,player1_time)
        end = time.time()
        player1_time = player1_time + end - start
        if player1_time > 120:
            winner = player2
            break
        # accept move?
        if not removing_verify(move,board_info,player1,player1,player2):
            winner = player2
            print 'Invalid move: ' + str(move)
            break
        # update board
        board_info[move[0] + 15][1] = 0
        board_info[move[0] + 15][2] = 0
        # tip?
        torque1,torque2,check_tip = tipping(board_info,grav_center,support1
                                            ,support2)
        if check_tip:
            winner = player2
            output(board_info,record,move,torque1,torque2)
            break

        output(board_info,record,move,torque1,torque2)
        step = step + 1

     # player 2
        board_info = np.loadtxt('board.txt')
        start = time.time()
        move = player_move(player2_arg,mode,player2,player2_time)
        end = time.time()
        player2_time = player2_time + end - start
        if player2_time > 120:
            winner = player1
            break
        # accept move?
        if not removing_verify(move,board_info,player2,player1,player2):
            winner = player1
            print 'Invalid move: ' + str(move)
            break
        # update board
        board_info[move[0] + 15][1] = 0
        board_info[move[0] + 15][2] = 0
        # tip?
        torque1,torque2,check_tip = tipping(board_info,grav_center,support1
                                            ,support2)
        if check_tip:
            winner = player1
            output(board_info,record,move,torque1,torque2)
            break
        output(board_info,record,move,torque1,torque2)
        step = step + 1

record.write(str(winner) + ' ' + str(player1_time)[:4] + ' ' +
             str(player2_time)[:4])

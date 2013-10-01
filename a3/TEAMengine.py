'''
Created on 28.09.2013

@author: Sven, Christian, Collin
'''

from subprocess import Popen, PIPE
import sys
import random
import pdb
import copy

infinity = 1.0e400

class NoTipping:
    
    def __init__(self):
        self.board = Board()
        self.to_move = 1
        self.utility = 0
        self.phase = 1
        self.valid_moves = self._get_valid_moves()
        self.non_tipping_moves = self._get_non_tipping_moves()
    
    
    def magic_alphabeta_search(self):
        if(len(self.non_tipping_moves[self.to_move])>0):
			parallel = 1
			if parallel:
				l = []
				for move in self.non_tipping_moves[self.to_move]:
					temp_board = copy.deepcopy(self.board.board)
					temp_board[move[0]] = move[1]
					x = []
					x.append(self.to_move*-1)
					x.append(self.phase)
					inp = x + temp_board[16:32] + temp_board[0:16]
					inp = map(lambda x : str(x), inp)
					# This is wrong! because list(str(self.to_move))
					l.append(Popen(['./TEAM.out'] + inp, stdout=PIPE))
				l = map(lambda x : x.communicate(), l)
				l = map(lambda x : (int(x[0].split(" ")[0]), 
									int(x[0].split(" ")[1]), 
									int(x[0].split(" ")[2])), l)
#                   pdb.set_trace()
				v = map(lambda x : x[2], l)
				i = v.index(min(v))
				return self.non_tipping_moves[self.to_move][i]
			else:
#                    pdb.set_trace()
				x = []
				x.append(self.to_move)
				x.append(self.phase)
				inp = x + self.board.board[16:32] + self.board.board[0:16]
				inp = map(lambda x : str(x), inp)
#                    print inp
				result = Popen(['./TEAM.out'] + inp, stdout=PIPE)
				result = result.communicate()
				ints = result[0].split(" ")
				return (int(ints[0]) - 15, int(ints[1]))
        else:
            return random.choice(self.valid_moves[self.to_move])

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return self.valid_moves

    def make_move(self, move):            
        if(self.phase==1):
            move = (move[0],self.to_move*abs(move[1]))
                
        if self.to_move == 1:
            if move not in self.valid_moves[1]:
            #DOES THIS HAVE TO BE A DEEP COPY?
                return self # Illegal move has no effect
        else:
            if move not in self.valid_moves[-1]:
                return self # Illegal move has no effect

        if(self.phase == 1):
            self.board.set_weight(move[0], move[1])
        else:
            self.board.remove_weight(move[0],move[1])
        self._update_utility()
        self._update_moves(move[0], move[1])
        if((self.phase==1) and \
           (len(self.valid_moves[1])==0) and \
           (len(self.valid_moves[-1])==0)):
            self.phase = 2
            
        if(self.phase == 2):
            self.valid_moves = self._get_valid_moves() 
        self.non_tipping_moves = self._get_non_tipping_moves()
            
        self.change_player()       
        
        return self
    
    def get_utility(self):
        return self.utility


    def _get_non_tipping_moves(self):
        non_tipping_moves_1 = []
        non_tipping_moves_2 = []
        
        for move in self.valid_moves[1]:
            if(self.board.tip_lookAhead(move,self.phase)):
                continue
            non_tipping_moves_1.append(move) 
            
        for move in self.valid_moves[-1]:
            if(self.board.tip_lookAhead(move, self.phase)):
                continue
            non_tipping_moves_2.append(move) 
                    
        return (0,non_tipping_moves_1,non_tipping_moves_2)

    def _get_valid_moves(self):
        if self.phase == 1:
            moves_p1 = []
            moves_p2 = []
            for x in range(-15, 16):
                for y in range(1, 13):
                    if self.board.valid_placement(x, y):
                        moves_p1.append((x, y))
                for y in range(-12, 0):
                    if self.board.valid_placement(x, y):
                        moves_p2.append((x, y))
            return (0, moves_p1, moves_p2)
        else:
            moves_p1 = []
            moves_p2 = []
            weights_left = self._weights_left_1()
            for x in range(-15, 16):
                if(self.board.board[x]!=0):
                    if self.board.board[x]<0:
                        if weights_left:
                            moves_p2.append((x,self.board.board[x]))
                        else:
                            moves_p1.append((x,self.board.board[x]))
                            moves_p2.append((x,self.board.board[x]))
                            
                    else:
                            moves_p1.append((x,self.board.board[x]))
                            moves_p2.append((x,self.board.board[x]))
                        

            return (0, moves_p1, moves_p2)
        
    def _weights_left_1(self):
        return sum(map(lambda x : x > 0, self.board.board))
        

    def _update_moves(self, pos, weight):
        move_1 = []
        move_2 = []
        if self.phase == 1:
            for (x, y) in self.valid_moves[1]:
                if x == pos or y == weight:
                    continue
                else:
                    move_1.append((x,y))
            for (x, y) in self.valid_moves[-1]:
                if x == pos or y == weight:
                    continue
                else:
                    move_2.append((x,y))
        else:
            for (x, y) in self.valid_moves[1]:
                if x == pos and y == weight:
                    continue
                else:
                    move_1.append((x,y))
            for (x, y) in self.valid_moves[-1]:
                if x == pos or y == weight:
                    continue
                else:
                    move_2.append((x,y))
        self.valid_moves = (0,move_1,move_2)
            

    def change_player(self):
        if self.to_move == 1:
            self.to_move = -1
        else:
            self.to_move = 1

    def terminal_test(self):
        "A state is terminal if it is won or there are no empty squares."
        return self.board.tipped() or (not self.board.moves_left())

    def _update_utility(self):
        if self.board.tipped():
            if self.to_move == 1:
                return -1
            if self.to_move == -1:
                return 1
        else:
            return 0

    def generate_children(self):
        "Return a list of legal (move, state) pairs."
        if(len(self.non_tipping_moves)>0):
            for move in self.non_tipping_moves[self.to_move]:
                yield (move, self.make_move(move))
        else:
            move = self.valid_moves[self.to_move][0]
            yield (move, self.make_move(move))

    def display(self):
        b1 = 0
        b2 = 0
        suppos0 = -3
        suppos1 = -1
        for x in range(-1*int(30/2), int(30/2)+1):
            if(x <= suppos0 - 1):
                b1 += 2
            if(x <= suppos1 - 1):
                b2 += 2

            if(self.board.board[x]>=0):
                if(x<= suppos0 - 1):
                    b1 += 1
                if(x<= suppos1 - 1):
                    b2 += 1
                print "",

            if(self.board.board[x]<10 and
                       self.board.board[x]>-10):
                if(x<= suppos0 - 1):
                    b1 += 1
                if(x<= suppos1 - 1):
                    b2 += 1
                print "",

            print self.board.board[x],
        print
        for x in range(-1*int(30/2), int(30/2)+1):
            if(x>=0):
                print "",
            if(x<10 and x>-10):
                print "",
            print x,
        print ""
        print " "*b1,self.board.supports[0], \
            (b2-b1-len(str(self.board.supports[0]))-1)*" ", \
            self.board.supports[1]
        print ''

    def get_input(self,player,phase):
        
        if int(player) == 2:
            self.to_move = -1
        else:
            self.to_move = 1
            
        self.phase = phase       
                    
        board = 31*[0]
        f = open("board.txt")
        lines = f.readlines()
        for line in lines:
            indices = line.split()
            
            pos = int(indices[0])
            weight = int(indices[1])
            player = int(indices[2])
            
            if player == 1:
                board[pos] = weight
                if(phase == 1):
                    if(weight>0):
                        self._update_moves(pos, weight)
            else:
                board[pos] = -weight
                if(phase == 1):
                    if(weight>0):
                        self._update_moves(pos, -weight)
        self.board.renew_board(board)
        self.non_tipping_moves = self._get_non_tipping_moves()
        if(phase == 2):
            self.valid_moves = self._get_valid_moves()
            self.non_tipping_moves = self._get_non_tipping_moves()
    

class Board():

    def __init__(self, weightsPos = [0]*25):
        self.board = 31 * [0]
        self.supports = [-9, -3]
        self.weightsPos = weightsPos
        self.board[-4] = 3
        self.weightsPos[0] = -4
        self.supports = self.updateTorques()
        
    def renew_board(self,board):
        for i in range(-15,16,1):
            self.board[i] = board[i]
            if(board[i]!=0):
                self.weightsPos[board[i]] = i
            if(i==-4):
                if(board[i]==3):
                    self.weightsPos[0] = -4 
        
        self.supports = self.updateTorques()

    def get_weights_set(self):
        raise NotImplemented

    def _set_weight(self, pos, weight):
        self.board[pos] = weight
        self.weightsPos[weight] = pos

    def set_weight(self, pos, weight):
        if(self.valid_placement(pos, weight)):
            self._set_weight(pos, weight)
        else:
            raise ValueError("Invalid placement")
        self.supports = self.updateTorques()
        
    def _remove_weight(self, pos, weight):
        self.board[pos] = 0
        self.weightsPos[weight] = 99

    def remove_weight(self, pos, weight):
        if(self.valid_removement(pos, weight)):
            self._remove_weight(pos, weight)
        else:
            raise ValueError("Invalid removement")
        self.supports = self.updateTorques()

    def valid_placement(self,pos, weight):
        return self.board[pos] == 0 and \
               self.weightsPos[weight] == 0
               
    def valid_removement(self,pos, weight):
        return abs(self.board[pos]) == abs(weight)

    def moves_left(self):
        try:
            self.board.index(0)
        except ValueError:
            return False
        return True

    def updateTorques(self):
        sup1 = -9
        sup2 = -3
        for i in range(-15, 16):
            if i < -3:
                sup1 += abs(i + 3) * abs(self.board[i])
            else:
                sup1 -= abs(i + 3) * abs(self.board[i])
        for i in range(-15, 16):
            if i < -1:
                sup2 += abs(i + 1) * abs(self.board[i])
            else:
                sup2 -= abs(i + 1) * abs(self.board[i])
        return [sup1,sup2]

    def tipped(self):
        if self.supports[0] > 0 and self.supports[1] == 0:
            return True
        return (self.supports[0]*self.supports[1] > 0)


    def tip_lookAhead(self, move, phase):
        sup1 = self.supports[0]
        sup2 = self.supports[1]
        
        pos = move[0]
        weight = move[1]
        
        if phase == 1:
            if pos < -3:
                sup1 += abs(pos + 3) * abs(weight)
            else:
                sup1 -= abs(pos + 3) * abs(weight)
            if pos < -1:
                sup2 += abs(pos + 1) * abs(weight)
            else:
                sup2 -= abs(pos + 1) * abs(weight)
        else:
            if pos < -3:
                sup1 -= abs(pos + 3) * abs(weight)
            else:
                sup1 += abs(pos + 3) * abs(weight)
            if pos < -1:
                sup2 -= abs(pos + 1) * abs(weight)
            else:
                sup2 += abs(pos + 1) * abs(weight)
            
        if sup1 > 0 and sup2 == 0:
            return True
        return (sup1*sup2 > 0)



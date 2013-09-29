from utils import *
import random

# Minimax Search

def minimax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Fig. 6.4]"""

    player = game.to_move(state)

    def max_value(state):
        suc = game.successors(state)
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for (a, s) in suc:
            v = max(v, min_value(s))
        return v

    def min_value(state):
        suc = game.successors(state)
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for (a, s) in suc:
            v = min(v, max_value(s))
        return v

    # Body of minimax_decision starts here:
    suc = game.successors(state)
    action, state = argmax(suc,
                           lambda ((a, s)): min_value(s))
    return action



def alphabeta_full_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Fig. 6.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        suc = game.successors(state)
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -infinity
        for (a, s) in suc:
            v = max(v, min_value(s, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        suc = game.successors(state)
        if game.terminal_test(state):
            return game.utility(state, player)
        v = infinity
        for (a, s) in suc:
            v = min(v, max_value(s, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    suc = game.successors(state)
    action, state = argmax(suc,
                           lambda ((a, s)): min_value(s, -infinity, infinity))
    return action

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    action, state = argmax(game.successors(state),
                           lambda ((a, s)): min_value(s, -infinity, infinity, 0))
    return action

# Players for Games

def query_player(game, state):
    "Make a move by querying standard input."
    game.display(state)
    return num_or_str(raw_input('Your move? '))

def random_player(game, state):
    "A player that chooses a legal move at random."
    return random.choice(game.legal_moves())

def alphabeta_player(game, state):
    return alphabeta_search(state, game)

def play_game(game, *players):
    "Play an n-person, move-alternating game."
    state = game.initial
    while True:
        for player in players:
            move = player(game, state)
            state = game.make_move(move, state)
            if game.terminal_test(state):
                return game.utility(state, players[0])

# Some Sample Games

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test. You may
    override display and successors or you can inherit their default
    methods. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
#        abstract
        return

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
  #      abstract
        return

    def utility(self, state, player):
        "Return the value of this final state to player."
  #      abstract
        return

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
        
class NoTipping(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self):
        self.board = Board()
        self.board.initialize()
        self.dim = 30
        
        moves1 = [(x, y) for x in range(-15,16) if self.board.positionFree(x) for y in range(1,8) if not self.board.weightSet(y) and y != 0]
        moves2 = [(x, y) for x in range(-15,16) if self.board.positionFree(x) for y in range(-7,0) if not self.board.weightSet(y) and y != 0]
        self.initial = Struct(to_move=1, utility=0, moves=(0,moves1,moves2))
        

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def make_move(self, move, state, board = None):
        #print move
        if(state.to_move == 1):            
            if move not in state.moves[1]:
                return state # Illegal move has no effect
        else:
            if move not in state.moves[-1]:
                return state # Illegal move has no effect
        
        if board == None:
            board = Board(self.board.dim,self.board.positions[:],self.board.supports[:],self.board.weightsSet[:],self.board.weightsPos[:])
            
        ut = self.compute_utility(board, move, state)
        board.setWeight(move[0], move[1])
        moves = ([(x,y) for (x,y) in state.moves[1] if not move[0] == x and not move[1] == y],[(x,y) for (x,y) in state.moves[-1] if not move[0] == x and not move[1] == y])
        return Struct(to_move=if_(state.to_move == 1, -1, 1),
                      utility=ut,
                      moves=moves)

    def utility(self, state, player):
        "Return the value to X; 1 for win, -1 for loss, 0 otherwise."
        return state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self):
        b1 = 0
        b2 = 0
        for x in range(-1*int(self.dim/2), int(self.dim/2)+1):
            if(x<=self.board.supports[0]['pos']-1):
                b1 += 2
            if(x<=self.board.supports[1]['pos']-1):
                b2 += 2
                
            if(self.board.positions[x]>=0):
                if(x<=self.board.supports[0]['pos']-1):
                    b1 += 1
                if(x<=self.board.supports[1]['pos']-1):
                    b2 += 1
                print "",
                
            if(self.board.positions[x]<10 and self.board.positions[x]>-10):
                if(x<=self.board.supports[0]['pos']-1):
                    b1 += 1
                if(x<=self.board.supports[1]['pos']-1):
                    b2 += 1
                print "",
                
            print self.board.positions[x],
        print 
        for x in range(-1*int(self.dim/2), int(self.dim/2)+1):    
            if(x>=0):
                print "",
            if(x<10 and x>-10):
                print "",        
            print x,
        print ""
        print " "*b1,self.board.supports[0]['torque'],(b2-b1-len(str(self.board.supports[0]['torque']))-1)*" ",self.board.supports[1]['torque']
        print ''

        
    def compute_utility(self, board, move, state):
        "If X wins with this move, return 1; if O return -1; else return 0."
        bo = Board(board.dim,board.positions[:],board.supports[:],board.weightsSet[:],board.weightsPos[:])
        bo.setWeight(move[0],move[1])
        
        if (board._tipped()):
            return if_(state.to_move == -1, +1, -1)
        else:
            return 0
        
    def successors(self, state):
        "Return a list of legal (move, state) pairs."
       # print [(move, self.make_move(move, state))
        #        for move in state.moves[state.to_move]]
        print "DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONEE"
        return [(move, self.make_move(move, state))
                for move in state.moves[state.to_move]]

    
class Board():    
    
        def __init__(self, dim = 30, positions = None, supports = None, weightsSet = [0]*15, weightsPos = [0]*15):
            if positions == None:
                self.positions = [0] * (dim + 1)
            else:        
                self.positions = positions
            
            if supports == None:
                sup1 = {}
                sup2 = {}
                supports = [sup1,sup2]

            self.supports = supports
                
            self.dim = dim            
            self.weightsSet = weightsSet
            self.weightsPos = weightsPos   
            

        def initialize(self, t1=-3, t2=-1, inW = (-4,3)):        
            self.supports[0]['pos'] = t1
            self.supports[0]['torque'] = -9
                       
            self.supports[1]['pos'] = t2
            self.supports[1]['torque'] = -3            
                         
            
            #The initial weight has index 0
            self.positions[inW[0]] = inW[1]
            self.weightsPos[0] = -4
            self.weightsSet[0] = 1 
            
            sup =  self.calculateTorques(self.positions)
            self.supports[0]['torque'] = sup[0]
            self.supports[1]['torque'] = sup[1]
                     
            
        def setWeight(self, pos, weight, positions = None, weightsSet = None, weightsPos = None, supports = None):
            if positions == None:
                positions = self.positions
                
            if weightsSet == None:
                weightsSet = self.weightsSet
            
            if weightsPos == None:
                weightsPos = self.weightsPos
                
            if supports == None:
                supports = self.supports
                
            w = weight
            if(not self.weightSet(w,weightsSet)):
                if(self.positionFree(pos,positions)):
                    weightsSet[w] = 1
                    weightsPos[w] = pos
                    positions[pos] = w
                else:
                    raise ValueError('Position already used')
            else:
                raise ValueError('Weight already used')
            
            sup =  self.calculateTorques(self.positions)
            supports[0]['torque'] = sup[0]
            supports[1]['torque'] = sup[1]
                    
            
        def positionFree(self,pos,positions=None):
            if positions == None:
                positions = self.positions
            if(positions[pos]!=0):
                return False
            return True
        
        def weightSet(self,weight,weightsSet=None):
            if weightsSet == None:
                weightsSet = self.weightsSet
            if(weightsSet[weight]==1):
                return True
            return False
        
        def calculateTorques(self, positions = None):
            if positions == None:
                positions = self.positions
            board = positions
            sup1 = -9
            sup2 = -3
            for i in range(-15, 16):
                if i < -3:
                    sup1 += abs(i + 3) * abs(board[i])
                else:                    
                    sup1 -= abs(i + 3) * abs(board[i])
            for i in range(-15, 16):
                if i < -1:                    
                    sup2 += abs(i + 1) * abs(board[i])
                else:                    
                    sup2 -= abs(i + 1) * abs(board[i])
            return (sup1,sup2)

        def _tipped(self, supports=None):
            if supports == None:
                supports = self.supports
            if supports[0]['torque'] > 0 and supports[1]['torque'] == 0:
                return True
            return (supports[0]['torque']*supports[1]['torque'] > 0)               
        
        
        
        
        
####################################################################################       
        
class Fig62Game(Game):
    """The game represented in [Fig. 6.2]. Serves as a simple test case.
    >>> g = Fig62Game()
    >>> minimax_decision('A', g)
    'a1'
    >>> alphabeta_full_search('A', g)
    'a1'
    >>> alphabeta_search('A', g)
    'a1'
    """
    succs = {'A': [('a1', 'B'), ('a2', 'C'), ('a3', 'D')],
             'B': [('b1', 'B1'), ('b2', 'B2'), ('b3', 'B3')],
             'C': [('c1', 'C1'), ('c2', 'C2'), ('c3', 'C3')],
             'D': [('d1', 'D1'), ('d2', 'D2'), ('d3', 'D3')]}
    utils = Dict(B1=3, B2=12, B3=8, C1=2, C2=4, C3=6, D1=14, D2=5, D3=2)
    initial = 'A'

    def successors(self, state):
        return self.succs.get(state, [])

    def utility(self, state, player):
        if player == 'MAX':
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        return state not in ('A', 'B', 'C', 'D')

    def to_move(self, state):
        return if_(state in 'BCD', 'MIN', 'MAX')

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self, h=3, v=3, k=3):
        update(self, h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(to_move='X', utility=0, board={}, moves=moves)

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def make_move(self, move, state):
        if move not in state.moves:
            return state # Illegal move has no effect
        board = state.board.copy(); board[move] = state.to_move
        moves = list(state.moves); moves.remove(move)
        return Struct(to_move=if_(state.to_move == 'X', 'O', 'X'),
                      utility=self.compute_utility(board, move, state.to_move),
                      board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to X; 1 for win, -1 for loss, 0 otherwise."
        return state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print board.get((x, y), '.'),
            print

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
            self.k_in_row(board, move, player, (1, 0)) or
            self.k_in_row(board, move, player, (1, -1)) or
            self.k_in_row(board, move, player, (1, 1))):
            return if_(player == 'X', +1, -1)
        else:
            return 0

    def k_in_row(self, board, move, player, (delta_x, delta_y)):
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0 # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n >= self.k

class ConnectFour(TicTacToe):
    """A TicTacToe-like game in which you can only make a move on the bottom
    row, or in a square directly above an occupied square.  Traditionally
    played on a 7x6 board and requiring 4 in a row."""

    def __init__(self, h=7, v=6, k=4):
        TicTacToe.__init__(self, h, v, k)

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return [(x, y) for (x, y) in state.moves
                if y == 0 or (x, y-1) in state.board]
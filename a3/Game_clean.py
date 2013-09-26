from utils import infinity, argmax, argmin, Struct
import random
import copy

def alphabeta_search(state, game, d=4, cutoff_test=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for (a, s) in game.children(state):
            v = max(v, min_value(s, alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for (a, s) in game.children(state):
            v = min(v, max_value(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state,depth: depth>d or 
		    game.terminal_test(state)))
    eval_fn = lambda state: game.utility(state, player)
    action, state = argmax(game.children(state),
                           lambda ((a, s)): 
			   min_value(s, -infinity, infinity, 0))
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
    override display and children or you can inherit their default
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

    def children(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__
        
class NoTipping(Game):
    """Play TicTacToe on an h x v board, with Max (first player) 
	playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    def __init__(self):
        self.board = Board()
        self.dim = 30
        
        moves1 = [(x, y) 
		for x in range(-15,16) 
			if self.board.positionFree(x) 
		for y in range(1,8) 
			if not self.board.weightSet(y)]
        moves2 = [(x, y) 
			for x in range(-15,16) 
				if self.board.positionFree(x) 
			for y in range(-7,0) 
				if not self.board.weightSet(y)]
        self.initial = Struct(to_move=1, utility=0, 
                                 moves=(0,moves1,moves2))
        

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
            board = Board(self.board.dim,
                          self.board.positions[:],
                          self.board.supports[:],
                          self.board.weightsSet[:],
                          self.board.weightsPos[:])
            
        ut = self.compute_utility(board, move, state)
        board.setWeight(move[0], move[1])
        moves = ([(x,y) 
                     for (x,y) in state.moves[1] 
                          if not move[0] == x and not move[1] == y],
                 [(x,y) for (x,y) in state.moves[-1] 
                          if not move[0] == x and not move[1] == y])
        return Struct(to_move=if_(state.to_move == 1, -1, 1),
                      utility=ut,
                      moves=moves)

    def utility(self, state, player):
        "Return the value to X; 1 for win, -1 for loss, 0 otherwise."
        return state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0
    
    def compute_utility(self, board, move, state):
        "If X wins with this move, return 1; if O return -1; 
         else return 0."
        bo = Board(board.dim,board.positions[:],
                   board.supports[:],
                   board.weightsSet[:],
                   board.weightsPos[:])
        bo.set_weight(move[0],move[1])
        
        if (board._tipped()):
            return if_(state.to_move == -1, +1, -1)
        else:
            return 0
        
    def children(self, state):
        "Return a list of legal (move, state) pairs."
	for move in state.moves[state.to_move]:
		yield (move, self.make_move(move, state))

    def display(self):
        b1 = 0
        b2 = 0
	suppos0 = -3
	suppos1 = -1
        for x in range(-1*int(self.dim/2), int(self.dim/2)+1):
            if(x <= suppos0 - 1):
                b1 += 2
            if(x <= suppos1 - 1):
                b2 += 2
                
            if(self.board.positions[x]>=0):
                if(x<= suppos0 - 1):
                    b1 += 1
                if(x<= suppos1 - 1):
                    b2 += 1
                print "",
                
            if(self.board.positions[x]<10 and 
               self.board.positions[x]>-10):
                if(x<= suppos0 - 1):
                    b1 += 1
                if(x<= suppos1 - 1):
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
        print " "*b1,self.board.supports[0],\
                  (b2-b1-len(str(self.board.supports[0]))-1)*" ",\
                  self.board.supports[1]
        print ''

        
class Board():    
    
        def __init__(self, weightsPos = [0]*15):
            self.board = 31 * [0]
            self.supports = [-9, -3]
            self.dim = dim        
            self.weightsPos = weightsPos   
            self.positions[-4] = 3
            self.weightsPos[0] = -4
	    self.updateTorques()
                     
	def get_weights_set(self):
	    raise NotImplemented

	def _set_weight(self, pos, weight):
            self.board[pos] = weight
            self.weightsPos[weight] = pos

        def set_weight(self, pos, weight):
            if(valid_move(pos, weight)):
            	 _set_weight(pos, weight)
            else
            	raise ValueError("Invalid move")
            self.updateTorques()
            
        def valid_move(self,pos, weight):
            return self.board[pos] == 0 and \
                   self.weightsPos[weight] == 0
        
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
            return (sup1,sup2)

        def _tipped(self):
            if supports[0] > 0 and supports[1] == 0:
                return True
            return (supports[0]*supports[1] > 0)               
        
        
        

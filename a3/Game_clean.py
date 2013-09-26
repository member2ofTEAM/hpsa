from utils import infinity, argmax, argmin
import random
import copy

def alphabeta_search(state, game, d=4):
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
    cutoff_test = lambda state,depth: depth>d or \
                                      state.terminal_test()
    eval_fn = lambda state: game.utility(state, player)
    action, state = argmax(game.children(state),
                           lambda ((a, s)):
                           min_value(s, -infinity, infinity, 0))
    return action

class NoTipping:
    """Play TicTacToe on an h x v board, with Max (first player)
	playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self):
        self.board = Board()
        self.to_move = 1
        self.utility = 0
        self.phase = 1
        self.valid_moves = self._get_valid_moves()

    def legal_moves(self, state):
        "Legal moves are any square not yet taken."
        return self.valid_moves

    def make_move(self, move):
        if self.to_move == 1:
            if move not in self.valid_moves[1]:
            #DOES THIS HAVE TO BE A DEEP COPY?
                return self # Illegal move has no effect
        else:
            if move not in self.valid_moves[-1]:
                return self # Illegal move has no effect

        d = copy.deepcopy(self)
        d.board.set_weight(move[0], move[1])
        d._update_utility()
        d._update_moves(move[0], move[1])
        d.change_player()

        return d

    def _get_valid_moves(self):
        moves_p1 = []
        moves_p2 = []
        for x in range(-15, 16):
            for y in range(1, 8):
                if self.board.valid_placement(x, y):
                    moves_p1.append((x, y))
            for y in range(-7, 0):
                if self.board.valid_placement(x, y):
                    moves_p2.append((x, y))
        return (0, moves_p1, moves_p2)

    def _update_moves(self, pos, weight):
        for (x, y) in self.valid_moves[1]:
            if x == pos or y == weight:
                del (x, y)
        for (x, y) in self.valid_moves[-1]:
            if x == pos or y == weight:
                del (x, y)

    def change_player(self):
        if self.to_move == 1:
            self.to_move = -1
        else:
            self.to_move = 1

    def terminal_test(self, state):
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

    def children(self):
        "Return a list of legal (move, state) pairs."
        for move in moves[self.to_move]:
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


class Board():

    def __init__(self, weightsPos = [0]*15):
        self.board = 31 * [0]
        self.supports = [-9, -3]
        self.weightsPos = weightsPos
        self.board[-4] = 3
        self.weightsPos[0] = -4
        self.updateTorques()

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
        self.updateTorques()

    def valid_placement(self,pos, weight):
        return self.board[pos] == 0 and \
               self.weightsPos[weight] == 0

    def moves_left(self):
        try:
            self.board.find(0)
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
        return (sup1,sup2)

    def tipped(self):
        if self.supports[0] > 0 and self.supports[1] == 0:
            return True
        return (self.supports[0]*self.supports[1] > 0)




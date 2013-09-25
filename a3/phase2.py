import itertools


class Decision(object):

    def __init__(self, board, mask):
        self.decisions = {key: value for (key, value) in [(a, b) for (a, b) in zip(range(1, 16), range(1, 16))]}
        self.board = board
        self.mask = mask
        for k in range(1, 15):
            self.decisions[k] = {}
            for s in self._kbits(15, k):
                self.decisions[k][s] = {}
        for s in self.decisions[1].keys():
            if self._tipped(s):
                self.decisions[1][s] = 0
            else:
                self.decisions[1][s] = 1



    def _kbits(self, n, k):
        for bits in itertools.combinations(range(n), k):
            s = ['0'] * n
            for bit in bits:
                s[bit] = '1'
            yield (''.join(s))

    def _get_state(self, conf):
        board = 31 * [0]
        i = 0
        for pos in self.mask:
            if conf[i] == '1':
                board[pos] = self.board[pos]
            i = i + 1
        return board

    def _get_torque(self, conf):
        torque0, torque1 = (-9, -3)
        board = self._get_state(conf)
        for i in range(-15, 16):
            if i < -3:
                torque0 -= abs(i + 3) * board[i]
            else:
                torque0 += abs(i + 3) * board[i]
        for i in range(-15, 16):
            if i < -1:
                torque1 += abs(i + 1) * board[i]
            else:
                torque1 -= abs(i + 1) * board[i]
        return (torque0, torque1)

    def _tipped(self, conf):
        torque = self._get_torque(conf)
        if torque[0] > 0 and torque[1] == 0:
            return True
        return (torque[0]*torque[1] > 0)



#if __name__ == "__main__":
board = 31 * [0]
board[-13] = 6
board[-11] = 3
board[-10] = 5
board[-9] = 1
board[-8] = 4
board[-4] = 3
board[-3] = 1
board[-2] = 2
board[-1] = 2
board[1] = 7
board[2] = 4
board[3] = 3
board[4] = 5
board[6] = 7
board[12] = 6

mask = [-13, -11, -10, -9, -8, -4, -3, -2, -1, 1, 2, 3, 4, 6, 12]
torque = (0, 0)
decision = Decision(board, mask)
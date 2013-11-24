import sys, pdb, random
from copy import deepcopy
from subprocess import Popen, PIPE

def get_input():
    board = 31*[0]
    weights = {-1:{}, 1:{}}
    f = open("board.txt")
    lines = f.readlines()
    sup1 = -9
    sup2 = -3
    for line in lines:
        indices = line.split()

        pos = int(indices[0])
        weight = int(indices[1])
        player = int(indices[2])

        if pos < -3:
            sup1 += abs(pos + 3) * abs(weight)
        else:
            sup1 -= abs(pos + 3) * abs(weight)
        if pos < -1:
            sup2 += abs(pos + 1) * abs(weight)
        else:
            sup2 -= abs(pos + 1) * abs(weight)

        if player == 1:
            board[pos] = weight
            weights[player][weight] = 1
        elif player == 2:
            board[pos] = -weight
            weights[player][-weight] = 1
        else:
            board[pos] = weight
    return (board, weights, [sup1, sup2])

def tipping(move, torque, phase):
    sup1 = torque[0]
    sup2 = torque[1]
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


def valid(move, board, weights, to_move, phase, torque):
    if phase == 1:
        return (not weights[to_move].get(move[1], 0)
                and not board[move[0]] and not tipping(move, torque, phase))
    else:
        return board[move[0]] and not tipping(move, torque)

def magic_alphabeta_search(to_move, board, weights, phase, moves, torque):
    parallel = 0
    if parallel:
        l = []
        for move in moves:
            if not valid(move, board, weights, to_move, phase, torque):
                continue
            temp_board = deepcopy(board)
            temp_board[move[0]] = move[1]
            x = []
            x.append(to_move*-1)
            x.append(phase)
            inp = x + temp_board[16:32] + temp_board[0:16]
            inp = map(lambda x : str(x), inp)
            # This is wrong! because list(str(self.to_move))
            l.append(Popen(['./TEAM.out'] + inp, stdout=PIPE))
        l = map(lambda x : x.communicate(), l)
        l = map(lambda x : (int(x[0].split(" ")[0]),
                            int(x[0].split(" ")[1]),
                            int(x[0].split(" ")[2])), l)
        v = map(lambda x : x[2], l)
        i = v.index(min(v))
        return self.non_tipping_moves[to_move][i]
    else:
        x = []
        x.append(to_move)
        x.append(phase)
        inp = x + board[16:32] + board[0:16]
        inp = map(lambda x : str(x), inp)
        result = Popen(['./TEAM.out'] + inp, stdout=PIPE)
        result = result.communicate()
        ints = result[0].split(" ")
        return (int(ints[0]) - 15, int(ints[1]))


if __name__ == "__main__":
    try:
        phase = int(sys.argv[1])
        player = int(sys.argv[2])
        if player == 2:
            player = -1
    except:
        print "Usage: {1} phase player".format(sys.argv[0])
        sys.exit(0)
    moves = [(y, x) for x in range(-12, 13) if x for y in range(-15, 16)]
    (board, weights, torque) = get_input()
    move = None
#    try:
    move = magic_alphabeta_search(player, board, weights, phase, moves, torque)
#    except:
#        pass
    if not move:
        move = random.choice(moves)
    print str(move[0]) + " " + str(abs(move[1]))

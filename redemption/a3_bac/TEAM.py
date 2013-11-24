import sys, pdb, random
from subprocess import Popen, PIPE

def get_input():
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
        elif player == 2:
            board[pos] = -weight
        else:
            board[pos] = weight

    return board

def magic_alphabeta_search(to_move, board, phase):
    inp = [to_move] + [phase] + board[16:32] + board[0:16]
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

    move = magic_alphabeta_search(player, get_input(), phase)

    print str(move[0]) + " " + str(abs(move[1]))


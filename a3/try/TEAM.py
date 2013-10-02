import sys                    
from subprocess import Popen, PIPE

f = open("board.txt")
lines = f.readlines()
board = []
for line in lines:
    board.append(line.split(" ")[1])

a = Popen(['TEAM.out'] + [sys.argv[1]] + [sys.argv[2]] + board, stdout = PIPE)
output = a.communicate()[0].split(" ")
print output[0] + " " + output[1]


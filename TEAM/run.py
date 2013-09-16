import subprocess
import sys
import time
import socket

t0 = time.time()
p = subprocess.Popen(["./exe", sys.argv[1]], stdout=subprocess.PIPE)
output, err = p.communicate()
print output
print time.time() - t0, "combined seconds until completion"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8080))
s.send(output)
s.close()


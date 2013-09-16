import subprocess
import sys
import time

t0 = time.time()
p = subprocess.Popen(["./exe", sys.argv[1]], stdout=subprocess.PIPE)
output, err = p.communicate()
print "TEAM"
print output.split("\n")[int(sys.argv[2]) - 1]
#print time.time() - t0, "combined seconds until completion"


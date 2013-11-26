from subprocess import Popen
import sys

if __name__ == "__main__":
    try:
        mode = str(sys.argv[1])
        port = int(sys.argv[2])
    except:
        print "Usage: {0} mode port".format(sys.argv[0])
        sys.exit(0)
    if mode == "P":
        Popen(["python", "TEAM.py", str(mode), str(port)])
    if mode == "H":
        Popen(["java", "-jar", "Brievasion.jar", str(mode), str(port)])

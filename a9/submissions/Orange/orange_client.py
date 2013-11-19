import os
import socket
import sys
import random
 
 
def receive():
    msg = ''
    while '<EOM>' not in msg:
        chunk = s.recv(1024)
        if not chunk:
            break
        if chunk == '':
            raise RuntimeError("socket connection broken")
        msg += chunk
    msg = msg[:-5]
    return msg
 
 
if __name__ == "__main__":
    os.system("make")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', int(sys.argv[1])))
    print receive()
    s.send("Orange")
    print "Sent 'Orange'"
    input = receive()
    #print input
   
    params = input.split()
    if len(params) < 5:
      raise RuntimeError("client error: only received " + str(len(params)) + " params from server)")
    
    player_id = params[0]
    no_players = params[1]
    no_types = params[2]
    goal = params[3]
   
    orange_file = open("orange_input.txt", "w", 0)
    orange_file.write(' '.join(params[4:]))
    
    os.system("./orange %s %s %s %s 0" % (player_id, no_players, no_types, goal))
    response = open("orange_output.txt", "r").read()
    print "Sending bid:", response
    s.send(response)
    
    while(True):
        try:
            inc = receive()
        except socket.error:
            break
        if not inc:
            break
        #print inc
        orange_file = open("orange_input.txt", "w", 0)
        orange_file.write(inc)
        
        os.system("./orange %s %s %s %s 1" % (player_id, no_players, no_types, goal))
        response = open("orange_output.txt", "r").read()
        print "Sending bid:", response
        s.send(response)

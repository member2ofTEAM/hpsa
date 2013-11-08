#!/usr/bin/env python 

""" 
A simple echo server 
"""

'''Protocol: 
S:Name?
C:<TEAM_NAME>
S:<no_players> <goal> <no_types> <item_list> #Example: 3 3 4 0 0 1 2 3 2 1 3 2 2 1

Three scenarios
1
C:<bid>
S:<winner_id> <player_budget>
2
C:<bid>
S:0 #The server is still waiting for all bids
3
C:<bid>
S:-1 #Nothing to bid on anymore

''' 

import socket
import sys 

if __name__ == "__main__":
    p = 3 #No of players
    k = 4 #No of types
    n = 3 #Goal: obtain n items of any type
    budget = 100 #Money per player
    host = '' 
    port = int(sys.argv[1])
    backlog = 5 
    size = 1024 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog) 
    while 1: 
        client, address = s.accept() 
        data = client.recv(size) 
        if data: 
            client.send(data) 
        client.close()



#!/usr/bin/env python 

""" 
A simple echo server 
"""

'''Protocol: 
S:Name?
C:<TEAM_NAME>
S:<player_id> <no_players> <no_types> <goal> <item_list> #Example: 1 3 3 4 0 0 1 2 3 2 1 3 2 2 1
C:<bid>
S:<winner_id> <winner_budget> <player_budget>
.
.
.
''' 

import socket
import sys 
import pdb

def list_to_flat_string(l):
    result = ""
    for item in l:
        result += str(item) + " "
    return result[:-1]

def send_to_client(client, msg):
    msg += "<EOM>"
    client.send(msg)


if __name__ == "__main__":
    p = 1 #No of players
    k = 4 #No of types
    n = 3 #Goal: obtain n items of any type
    budget = 100 #Money per player
    host = '' 
    port = int(sys.argv[1])
    backlog = 5 
    size = 1024 
    item_list = [0, 1, 2, 3, 2, 1, 0, 2, 3, 1, 0]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host,port)) 
    s.listen(backlog)
    pdb.set_trace()
    players = {}
    for i in range(p): 
        client, address = s.accept()
        send_to_client(client, "Name?")
        name = client.recv(size) 
        players[i] = (name, budget, client)
        greeting = [i, p, k, n] + item_list
        client.send(list_to_flat_string(greeting)) 
        client.close()
    for item in item_list:
        bids = {}
        while(len(bids.values()) < len(players)):
            client, address = s.accept()
            bid_str = client.recv(size)
            try:
                [i, bid] = map(int, bid_str.split(" "))
                players[i][2] = client
            except ValueError:
                print "Invalid Bid: " + bid_str 
            try:
                if i not in bids:
                   if players[i][1] >= bid:
                       bids[i] = bid
                       print "Player " + players[i][0] + " bid " + str(bid) + "."
                   else:
                       bids[i] = 0
            except IndexError:
                print "Invalid Player number: " + str(i)

        highest_bid = max(bids.values())
        winner = dict((bid, i) for (i, bid) in bids.iteritems())[highest_bid]
        for i in range(p):
            players[i][2].send(list_to_flat_string([winner, players[winner][1], players[i][1]]))
            players[i][2].close()

            

    s.close()
    
    











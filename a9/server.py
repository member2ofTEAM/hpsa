#!/usr/bin/env python

"""
An echo server that uses threads to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import threading
import time
from Queue import Queue

class Server:
    def __init__(self, p, k, n):
        self.host = ''
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
       
        #Game specific attributes
        self.p = p
        self.k = k 
        self.n = n 
        self.item_list = [0, 1, 2, 3, 2, 1, 0, 2, 3, 1, 0]
 
    def list_to_flat_string(l):
         result = ""
         for item in l:
             result += str(item) + " "
         return result[:-1]
       
    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(self.backlog)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        while (len(self.threads) < self.p):
            player_id = len(self.threads)
            client, address = self.server.accept
            client.send("Name?")
            name = client.recv(Client.size)
            greeting = [player_id, self.p, self.k, self.n] + self.item_list 
            client.send(list_to_flat_string(greeting))
            c = Client((client, address), player_id, name)
           c.start()
            self.threads.append(c)
        
        for item in self.item_list:
            bids = []
            for client in threading.enumerate(self.threads):
                #Prevent the client from trying to read in auction results
                client.waiting_lock.acquire()
                #Wait for the client to receive its bid
                client.ready_lock.acquire()
                #Read the bid
                bids.append(client)
            highest_bid = max(bids, key=lambda x: x.bid)
            highest_bidder = [client for client in bids if client.bid = highest_bid]
            #If two player have the same timestamp, the one with the lower player id is chosen
            winner = min(highest_bidder, key=lambda x.time)
            for client in threding.enumerate(self.threads):
                client.bid_result[0] = winner.player_id
                #The winner doesn't know it won yet, so we have to subtract the bid
                client.bid_result[1] = winner.budget - bid
                #Let the client continue
                client.waiting_lock.release()

                  
        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    self.size = 1024

    def __init__(self,(client,address), player_id, name):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        #Game specific attributes
        self.budget = 100
        self.player_id = player_id
        self.name = name
        #-1 means no bid has been received yet from this client
        self.bid = 0
        self.bid_time
        self.bid_result = [0, 0]
        self.ready_lock = threading.Lock()
        self.waiting_lock = threading.Lock()
        self.time = 120000

    def run(self):
        running = 1
        while (1):
            self.ready_lock.acquire()
            before = time.time()
            bid = self.client.recv(self.size)
            after = time.time()
            self.time -= after - before
            if self.time <= 0:
                print "Player " + str(self.name) + " timed out and is disqualified."
            if bid:
                try:
                    bid = int(bid)
                except ValueError:
                    print "Player " + str(self.name) + "sent invalid bid: " + bid,
                    print " and is disqualified."
                    break
                if bid > self.budget:
                    self.bid = 0
                else:
                    self.bid = bid
            else:
                self.client.close()
                print "Player " + str(self.name) + "disconnected and is disqualified."
                break
            #If I bid ealier than my competitor I'd win
            self.bid_time = time.time()
            #Now I want to communicate my bid and receive the result
            self.ready_lock.release()

            self.waiting_lock.acquire()
            [winner_id, winner_budget] = self.bid_result
            if self.player_id == winner_id:
                self.budget -= self.bid
            self.waiting_lock.release()
                        

if __name__ == "__main__":
    s = Server()
    s.run()



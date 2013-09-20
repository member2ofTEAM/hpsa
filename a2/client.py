'''
Created on Sep 20, 2013

@author: shaqal
'''
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 5006))
ques1=s.recv(1024)

if ques1=="Team_Name?":
    s.send("Shaqal")

input_data=''

while True:
    chunk = s.recv(1000000)
    if not chunk: break
    if chunk == '':
        raise RuntimeError("socket connection broken")
    input_data = input_data + chunk
    if ';' in input_data:
        break

#calculate your solution is less than 2 minutes
solution = "1 2 3 4 54 77 43 3 4 5 6 7 8 9;"

totalsent=0
MSGLEN = len(solution) 
while totalsent < MSGLEN:

    sent = s.send(solution[totalsent:])
    if sent == 0:
        raise RuntimeError("socket connection broken")
    totalsent = totalsent + sent

s.close()
'''
Created on Sep 20, 2013

@author: shaqal
'''
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 5006))
ques1=s.recv(1024)

if ques1=="Team_Name?":
    s.send("TEAM")

input_data=''

while True:
    chunk = s.recv(1000000)
    if not chunk: break
    if chunk == '':
        raise RuntimeError("socket connection broken")
    input_data = input_data + chunk
    if ';' in input_data:
        break

input_data = input_data.replace(";", "")
f = open('input.dat', 'wb')
f.write(input_data)
execfile('program.py')
f.close()

f = open('result.dat', 'rb')
solution = f.read()
f.close()

totalsent=0
MSGLEN = len(solution) 
while totalsent < MSGLEN:

    sent = s.send(solution[totalsent:])
    if sent == 0:
        raise RuntimeError("socket connection broken")
    totalsent = totalsent + sent

s.close()

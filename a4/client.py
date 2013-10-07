'''
@author: akshay
'''
import socket, sys

teamName = "TeamTeam"
eom = "<EOM>"
port = 5555
maxlen = 999999

if sys.argv[1]:
  port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', port))

inpData=''
sampleResult = """hospitals 0 (37,35); 1 (2,48); 2 (94,61); 3 (48,12); 4 (60,68)
ambulance 0  269 (37,34,169); 126 (34,40,87);115 (31,39,110);188 (30,35,138);(37,35)
ambulance 0  111 (42,38,103); 175 (45,44,87); (48,12)
ambulance 0  178 (31,44,157); (37,35)
ambulance 1  241 (40,28,100)
ambulance 1  230 (46,31,97)
ambulance 1  49 (53,33,72)
ambulance 1  103 (54,38,113)
ambulance 1  (37,35)
ambulance 20  73 (44,4,99);
ambulance 20  102 (38,7,104);140 (30,6,99);89 (30,3,127); (48,12)
ambulance 20  11 (59,9,144)
ambulance 20  215 (66,10,138)
ambulance 20  134 (66,5,164);(48,12)
"""

def getData(sock):
  inpData=''
  s.send(teamName)
  while True:
      chunk = sock.recv(maxlen)
      if not chunk: break
      if chunk == '':
          raise RuntimeError("socket connection broken")
      inpData = inpData + chunk
      if eom in inpData:
          break
  return inpData
  
def sendResult(sock,result):
  result += eom
  totalsent=0
  MSGLEN = len(result) 
  while totalsent < MSGLEN:
  
      sent = sock.send(result[totalsent:])
      if sent == 0:
          raise RuntimeError("socket connection broken")
      totalsent = totalsent + sent
  

inpData = getData(s)
sendResult(s,sampleResult)

reply = getData(s)
print reply


s.close()
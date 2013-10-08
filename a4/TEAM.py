'''
Created on 03.10.2013

@author: Sven, Christian, Colin
'''
#Comment
from numpy import array
from scipy.cluster.vq import kmeans
from subprocess import Popen, PIPE
from sys import argv
import socket
import pdb

teamName = "TEAM"
eom = "<EOM>"
port = 5555
maxlen = 999999

if argv[1]:
  port = int(argv[1])


    
def distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

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

    
class Hospital(): 
           
    def __init__(self, position, no_ambulances, id):
        self.position = position
        self.no_ambulances = no_ambulances
        self.id = id
                                
    def _sort_wrt(self,(p1, p2)):
        self.patients.sort(key=lambda x: distance(x.position, [p1, p2]))
        
    def __str__(self):
        return str(self.id) + " (" + str(self.position[0]) + ", " + str(self.position[1]) +")"

class Patient():
  
    def __init__(self, position, time, id):
        self.position = position
        self.time = time
        self.id = id

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', port))
all_patients = []
data = []
id = 0
lines = getData(s).split("\n")
for line in lines[1:301]:
    if line != "\n": 
        line.strip()
        temp = line.split(',')
        all_patients.append(Patient((int(temp[0]), int(temp[1])), int(temp[2]),id))
        data.append([int(temp[0]), int(temp[1])])
        id = id + 1

hosp_ambulances = map(int, lines[304:309])
hosp_ambulances = zip(hosp_ambulances, range(5))
hosp_ambulances.sort(key = lambda x: int(x[0]))

sendResult(s, "")
getData(s)

total_score = 0
best_j = 0
best_time = 0
for trash in range(10):
    print trash
    for meansscale in range(100, 101, 5):
        meansscale = float(meansscale) / 100.0;
        for timefactor in range(1):
            times = []
            patients = all_patients
            ambulances = []
                                    
            means = kmeans(array(data), 5, 100)[0]
            cluster_distances = []
            
            data = [patient.position for patient in patients if patient.time<120]
            urg_means = list(kmeans(array(data),5,100)[0])
            
            for i in range(len(means)):
                l = map(lambda x: distance(x, means[i]), urg_means)
                j = l.index(min(l))
                means[i] = (((urg_means[j][0] - means[i][0]) * meansscale)+means[i][0], 
                            ((urg_means[j][1] - means[i][1]) * meansscale)+ means[i][1])
                del urg_means[j]
            
            
            for mean in means:
                cluster_distance = []
                for patient in patients:
                        cluster_distance.append(distance(patient.position, mean))
                cluster_distances.append([sum(cluster_distance)] + list(mean))
                
            cluster_distances.sort(key=lambda x: int(x[0]))
            
            hospitals = []
            
            def sort_wrt((p1, p2)):
                patients.sort(key=lambda x: distance(x.position, [p1, p2]))
                
            for i in range(len(cluster_distances)):
                h = [cluster_distances[i][1], cluster_distances[i][2]]
                sort_wrt(h)
                hospitals.append(Hospital((h[0], h[1]), hosp_ambulances[i][0], hosp_ambulances[i][1]))

            patients.sort(key=lambda x: x.id)

            f = open("TEAMinput.txt", "wb")
            for patient in patients:
                f.write(str(patient.position[0]) + " " +
                        str(patient.position[1]) + " " +
                        str(patient.time) + "\n")

            hospitals.sort(key=lambda x: x.id)
            for hospital in hospitals:
                f.write(str(hospital.position[0]) + " " +
                        str(hospital.position[1]) + " " + 
                        str(hospital.no_ambulances) + "\n")
            f.close()
 
            total_saves = 0
            l = [Popen(["./TEAM"], stdout = PIPE) for x in range(8)]
            outputs = map(lambda x: x.communicate()[0].split("\n"), l)
            for output in outputs:
                ambulances = output[:-1]
                #print "Our saves: " + output[-1]

                result = "hospitals "
                for hospital in hospitals:
                    result = result + str(hospital.id) + " (" + \
                                    str(hospital.position[0]) + ", " + \
                                    str(hospital.position[1]) + "); "
                result = result[:-2] + "\n"
                for ambulance in ambulances:
                    result = result + str(ambulance) + "\n"

                #our output
                print output[-1]

#TODO SAVE BEST RESULT!!!
#TODO MAKE SCORE INDEPENDENT OF SERVER REPLY!
#TODO REMOVE AMBULANCE RESTRICTION IN C FILE

#TODO IMPLEMENT THE MEANS STUFF!

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', port))
                getData(s)
                sendResult(s, result)
                reply = getData(s)
                #print reply
                total_saves = max(int(reply.split("\n")[0].split(" ")[-1]), total_saves)
 
            if total_saves > total_score:
                total_score = total_saves
                best_j = float(meansscale)
                best_time = timefactor 
                
                print "total_score " + str(total_score)
                print "best ratio " + str(best_j)
                print "best time-factor " + str(best_time)
    
   
 

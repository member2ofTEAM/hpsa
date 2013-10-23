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
from time import time
from scipy.stats.mstats import mquantiles

teamName = "TEAM"
eom = "<EOM>"
port = 5555
maxlen = 999999
TIME_CUTOFF = 105

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

def _sort_wrt(list1, list2):
    for i in range(len(list1)):
        l = map(lambda x: distance(x, list1[i]), list2[i:])
        j = l.index(min(l)) + i
        (list2[i], list2[j]) = (list2[j], list2[i])

start_time = time()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', port))
all_patients = []
data = []
urgencies = []
id = 0
lines = getData(s).split("\n")
for line in lines[1:301]:
    if line != "\n": 
        line.strip()
        temp = line.split(',')
        all_patients.append(Patient((int(temp[0]), int(temp[1])), int(temp[2]),id))
        data.append([int(temp[0]), int(temp[1])])
        urgencies.append(int(temp[2]))
        id = id + 1

urgency_quants = list(mquantiles(array(urgencies), [0.25, 0.5, 0.75, 1]))

hosp_ambulances = map(int, lines[304:309])
hosp_ambulances = zip(hosp_ambulances, range(5))
hosp_ambulances.sort(key = lambda x: int(x[0]))

very_urgent = array([patient.position for patient in all_patients if patient.time<urgency_quants[0]])
urgent      = array([patient.position for patient in all_patients if patient.time<urgency_quants[1]])
bulk        = array([patient.position for patient in all_patients if patient.time>urgency_quants[1] and patient.time<urgency_quants[2]])
all         = array([patient.position for patient in all_patients])

mean_weights = [[4, 2, 1, 0],
                [2, 4, 4, 1],
                [1, 2, 6, 2],
                [0, 1, 2, 5], 
                [0, 1, 0, 1]]

total_score = 0
best_j = 0
best_time = 0
best_result = ""
best_saves = 0
for trash in range(10):
    if (time() - start_time > TIME_CUTOFF):
        break;
    all_means = list(kmeans(all, 5, 100)[0])
    very_urgent_means = list(kmeans(very_urgent, 5, 100)[0])
    urgent_means = list(kmeans(urgent, 5, 100)[0])
    bulk_means = list(kmeans(bulk, 5, 100)[0])
    _sort_wrt(all_means, very_urgent_means)
    _sort_wrt(all_means, urgent_means)
    _sort_wrt(all_means, bulk_means)
    means = 5 * [0]
    print trash
#    for meansscale in range(0, 101, 20):
#        meansscale = float(meansscale) / 100.0;
    for weight_config in range(4):
#        urgent_means = list(kmeans(urgent, 5, 50)[0])
        _sort_wrt(all_means, urgent_means)

        for timefactor in range(1):
            if (time() - start_time > TIME_CUTOFF):
                break;
            times = []
            patients = all_patients
            ambulances = []
            cluster_distances = []

            mw = mean_weights[weight_config]
#            mw = mean_weights[4]
            for i in range(len(means)):
                means[i] = ((very_urgent_means[i][0] * mw[0] + 
                                  urgent_means[i][0] * mw[1] + 
                                    bulk_means[i][0] * mw[2] + 
                                     all_means[i][0] * mw[3])/sum(mw),
                            (very_urgent_means[i][1] * mw[0] + 
                                  urgent_means[i][1] * mw[1] + 
                                    bulk_means[i][1] * mw[2] + 
                                     all_means[i][1] * mw[3])/sum(mw))
                means[i] = (int(round(means[i][0])), int(round(means[i][1])))

            #THIS IS NOT FACTORING URGENCY AT ALL
            #TODO WE HAVE TO MODIFY THE WAY WE ASSIGN AMBULANCES
            mw = mean_weights[weight_config]
	    for mean in means:
                cluster_distance = 4*[[]]
                for patient in very_urgent:
                        cluster_distance[0].append(distance(tuple(patient), mean))
                for patient in urgent:
                        cluster_distance[1].append(distance(tuple(patient), mean))
                for patient in bulk:
                        cluster_distance[2].append(distance(tuple(patient), mean))
                for patient in all:
                        cluster_distance[3].append(distance(tuple(patient), mean))
                sumcdist = sum(map(lambda x, y: sum(x)*y, cluster_distance, mw))
                cluster_distances.append([sumcdist] + list(mean))
                
            cluster_distances.sort(key=lambda x: int(x[0]))


#            for i in range(len(means)):
#                l = map(lambda x: distance(tuple(x), all_means[i]), urgent_means)
#                j = l.index(min(l))
#                means[i] = (((urgent_means[j][0] - all_means[i][0]) * meansscale) + all_means[i][0],
#                            ((urgent_means[j][1] - all_means[i][1]) * meansscale) + all_means[i][1])
#                del urgent_means[j]
#                means[i] = (int(round(means[i][0])), int(round(means[i][1])))


#            for mean in means:
#                cluster_distance = []
#                for patient in patients:
#                        cluster_distance.append(distance(patient.position, mean))
#                cluster_distances.append([sum(cluster_distance)] + list(mean))

#            cluster_distances.sort(key=lambda x: int(x[0]))

            
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
            l = [Popen(["taskset"] + ["-c"] + [str(x)] + ["./TEAM"], stdout = PIPE) for x in range(8)]
            outputs = map(lambda x: x.communicate()[0].split("\n"), l)
            for output in outputs:
                ambulances = output[:-1]
                total_saves = int(output[-1])

                result = "hospitals "
                for hospital in hospitals:
                    result = result + str(hospital.id) + " (" + \
                                    str(hospital.position[0]) + ", " + \
                                    str(hospital.position[1]) + "); "
                result = result[:-2] + "\n"
                for ambulance in ambulances:
                    result = result + str(ambulance) + "\n"

                if total_saves > best_saves:
                    best_saves = total_saves
                    best_result = result

                print output[-1]

                if (time() - start_time > TIME_CUTOFF):
                    break;
 

#TODO REMOVE AMBULANCE RESTRICTION IN C FILE

#TODO IMPLEMENT THE MEANS STUFF!
   
print best_result 
sendResult(s, best_result)
reply = getData(s)
print reply

 

'''
Created on 03.10.2013

@author: Sven
'''

from numpy import array
from scipy.cluster.vq import kmeans

def distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])
    
class Hospital(): 
           
    def __init__(self, position, patients, no_ambulances, id):
        self.position = position
        self.patients = patients 
        self.no_ambulances = no_ambulances
        self.ambulances = []
        self.id = id
        for i in range(self.no_ambulances):
            self.ambulances.append(Ambulance(self.position))
                                
    def _sort_wrt(self,(p1, p2)):
        self.patients.sort(key=lambda x: distance(x.position, [p1, p2]))
        
    def assign_patients(self):
        pos_patients = [patient.position for patient in self.patients]
        clusters = kmeans(array(pos_patients), len(self.ambulances), 100)[0]
        no = int(round(len(self.patients) / len(self.ambulances)))
        for i in range(len(self.ambulances)):
            clust = clusters[i]
            self._sort_wrt(clust)
            for j in range(no):
                try:
                    self.ambulances[i].assign(self.patients[0])
                    del self.patients[0]
                except IndexError:
                    assert i == len(self.ambulances) - 1

    def __str__(self):
        return str(self.id) + " (" + str(self.position[0]) + ", " + str(self.position[1]) +")"


class Patient():
  
    def __init__(self, position, time, id):
        self.position = position
        self.time = time
        self.init_time = time
        self.id = id
    
    def __str__(self):
        return str(self.id) + " (" + str(self.position[0]) + ", "  + str(self.position[1]) + ", " + str(self.init_time) + ")"
        
class Ambulance():
    
    def __init__(self, pos):
        self.pos = pos
        self.start = pos
        self.route = []
        self.patients = []
        
    def assign(self, patient):
        self.patients.append(patient)
        
    def _sort_wrt(self,(p1, p2),timefactor=0):
        self.patients.sort(key=lambda x: distance(x.position, [p1, p2])*(x.time)^timefactor)
        #self.patients.sort(key=lambda x: x.time)
        
    def get_route(self,timefactor=0):
        if self.route:
            return self.route
        while(self.patients):
            route = []
            for i in range(4):
                if(len(route)>0):
                    time_left = min([patient.time for patient in route])
                else:
                    time_left = 300
                self._sort_wrt(self.pos,timefactor)
                if(not(self.patients)):
                    break
                if(time_left < distance(self.patients[0].position, self.pos) + distance(self.patients[0].position, self.start) + 2):
                    break
                route.append(self.patients[0])
                time = distance(self.patients[0].position, self.pos)
                self.pos = self.patients[0].position
                del self.patients[0]
                self._update_time(time + 1)
                
            self._update_time(1 + distance(route[-1].position, self.start))             
            self.pos = self.start                
            
            self.route.append(route)

    
    def _update_time(self, time):
        temp = []
        for patient in self.patients:
             patient.time -= time
             if patient.time <= 0:
                 continue
             else:
                 temp.append(patient)
        self.patients = temp
                 

def print_result(hospitalss, filename):
    f = open(filename, 'wb')
    for i in range(len(hospitalss)):
        if i:
            f.write("; " + str(hospitalss[i]))
        else:
            f.write("hospitals " + str(hospitalss[i]))
    f.write("\n")
    id = 0
    hospitalss.sort(key=lambda x: int(x.id))
    for i in range(len(hospitalss)):
        for ambu in hospitalss[i].ambulances:
            for route in ambu.route:
                f.write("ambulance " + str(id) + " ")
                for patient in route:
                    f.write(str(patient) + "; ")
                f.write(str(hospitalss[i].position) + "\n")
            id = id + 1

total_score = 0
best_j = 0
best_time = 0
for i in range(1):
    print i
    for j in range(1):
        for k in range(1):
            data = []
            times = []
            patients = []
            ambulances = []
            hosp_ambulances = [(5,0), (9,1), (6,2), (11,3), (10,4)]
            
            hosp_ambulances.sort(key = lambda x: int(x[0]))
            
            id = 0
            f = open("ambusamp2010_2.txt", 'rb')
            s = f.read()
            for line in s.split("\n")[1:]:
                if line != "\n":
                    temp = line.split(',')
                    temp[2] = temp[2].replace("\n", "")
                    patients.append(Patient((int(temp[0]), int(temp[1])), int(temp[2]),id))
                    data.append([int(temp[0]), int(temp[1])])
                    id = id + 1
                        
            
            hospitals = kmeans(array(data), 5, 100)[0]
            cluster_distances = []
            
            urgent_patients = [patient for patient in patients if patient.time<120]
            
            data = []
            for up in urgent_patients:
                data.append(up.position)
            
            urg_hospitals = kmeans(array(data),5,100)[0]
            
            
            for i in range(len(hospitals)):
                dist = 100000
                best = (0,0)
                temp = []
                for urg_hospital in urg_hospitals:
                    new_dist = distance(hospitals[i],urg_hospital)
                    if new_dist < dist:
                        temp.append(best)
                        best = urg_hospital
                        dist = new_dist
                    else:
                        temp.append(urg_hospital)
                hospitals[i] = [hospitals[i][0] + int((hospitals[i][0]-best[0])*(float(j)/10)),hospitals[i][1] + int((hospitals[i][1]-best[1])*(float(j)/10))]
                urg_hospital = temp
            
            
            for hospital in hospitals:
                cluster_distance = []
                for patient in patients:
                        cluster_distance.append(distance(patient.position, hospital))
                cluster_distances.append([sum(cluster_distance), hospital[0], hospital[1]])
                
            cluster_distances.sort(key=lambda x: int(x[0]))
            
            hospitalss = []
            
            def sort_wrt((p1, p2)):
                patients.sort(key=lambda x: distance(x.position, [p1, p2]))
                
            for i in range(len(cluster_distances)):
                h = [cluster_distances[i][1],cluster_distances[i][2]]
                sort_wrt(h)
                no = int(round(300 * hosp_ambulances[i][0] / sum(map(lambda x : int(x[0]), hosp_ambulances))))
                if(no<len(patients)):
                    hospitalss.append(Hospital((h[0], h[1]) ,patients[0:no-1],  hosp_ambulances[i][0], hosp_ambulances[i][1]))
                else:
                    hospitalss.append(Hospital((h[1], h[2]), patients, hosp_ambulances[i][0], hosp_ambulances[i][1]))
                del patients[0:no-1]
            
            total_saves = 0
            
            for hospital in hospitalss:
                hospital.assign_patients()
                for ambulance in hospital.ambulances:
                    ambulance.get_route(k)
                    for route in ambulance.get_route():
                        total_saves += len(route)
                
            if total_saves > total_score:
                total_score = total_saves
                best_j = float(j)/float(10)
                best_time = k          
                print_result(hospitalss, "team_output.txt")
                
    print "total_score " + str(total_score)
    print "best ratio " + str(best_j)
    print "best time-factor " + str(best_time)
    
    
    
'''
data = []
times = []

for line in open("ambu2009.txt", 'r'):
    temp = line.split(',')
    data.append([int(temp[0])*int(temp[2]),int(temp[1])*int(temp[2])])
    times.append(int(temp[2]))
    
m = max(times)
    
k = kmeans(array(data),5,1000) 

newks = []

for centroid in k[0]:
    newks.append([centroid[0]/m,centroid[1]/m])
    
print "Means with Urgency-Multiplier" + str(newks)

for line in open("ambu2009.txt", 'r'):
    temp = line.split(',')
    data.append([int(temp[0]),int(temp[1])])
centroids = array([[80,20],[80,80],[20,20],[20,80],[50,50]])
print kmeans(array(data),centroids,1000)
'''

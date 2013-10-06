'''
Created on 03.10.2013

@author: Sven, Christian, Colin
'''
#Comment
from numpy import array
from scipy.cluster.vq import kmeans
import pdb

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
            self._sort_wrt(clusters[i])
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
        self.saved = 0
    
    def __str__(self):
        return str(self.id) + " (" + str(self.position[0]) + ", "  + str(self.position[1]) + ", " + str(self.init_time) + ")"
        
class Ambulance():
    
    def __init__(self, pos):
        self.pos = pos
        self.start = pos
        self.route = []
        self.patients = []
        self.all_patients = []
        
    def assign(self, patient):
        self.patients.append(patient)
        self.all_patients.append(patient)
        
    def _sort_wrt(self,(p1, p2),timefactor=0):
        self.patients.sort(key=lambda x: distance(x.position, [p1, p2])*(x.time)^timefactor)
        #self.patients.sort(key=lambda x: x.time)
        
    def _sort_hospitals(self,(p1,p2)):
        hospitals.sort(key=lambda x: distance(x.position,[p1,p2]))
        
    def get_route(self,timefactor=0):
        if self.route:
            return self.route
        while(self.patients):
            route = []
            hosp = self.start
            for i in range(4):
                
                if(not(self.patients)):
                    break
                                
                self._sort_wrt(self.pos,timefactor)
                time_left = 10000
                              
                self._sort_hospitals(self.patients[0].position)
                
                temp_hosp = hospitals[0].position
                
                
                if(route):
                    time_left = min([patient.time for patient in route])
                else:
                    if (distance(self.patients[0].position, self.pos) + \
                        distance(self.patients[0].position, temp_hosp) + 2 > self.patients[0].time):
                        del self.patients[0]
                        break

                if(time_left < distance(self.patients[0].position, self.pos) + \
                               distance(self.patients[0].position, temp_hosp) + 2):
                    break
                
                hosp = temp_hosp
                route.append(self.patients[0])
                time = distance(self.patients[0].position, self.pos)
                self.pos = self.patients[0].position
                del self.patients[0]
                self._update_time(time + 1)
                
            if route:
                self._update_time(1 + distance(route[-1].position, hosp)) 
                for patient in route:
                    if patient.time >= 0:
                        patient.saved = 1;    
                route.append(hosp)  
                self.route.append(route)
            self.pos = hosp

        hospitals.sort(key = lambda x: x.id)
        return self.route

    
    def _update_time(self, time):
        for patient in self.all_patients:
             patient.time -= time
        tmp = []
        for i in range(len(self.patients)):
            if self.patients[i].time >= 0:
                tmp.append(self.patients[i])
        self.patients = tmp


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
                    if(isinstance(patient,Patient)):
                        f.write(str(patient) + "; ")
                f.write(str(route[-1]) + "\n")
            id = id + 1

total_score = 0
best_j = 0
best_time = 0
for trash in range(10):
    print trash
    for meansscale in range(0, 101, 5):
        meansscale = float(meansscale) / 100.0;
        for timefactor in range(5):
            data = []
            times = []
            patients = []
            ambulances = []
            
            id = 0
            f = open("ambu2009_2.txt", 'rb')
            lines = f.read().split("\n")
            for line in lines[1:301]:
                if line != "\n": 
                    line.strip()
                    temp = line.split(',')
                    patients.append(Patient((int(temp[0]), int(temp[1])), int(temp[2]),id))
                    data.append([int(temp[0]), int(temp[1])])
                    id = id + 1

            hosp_ambulances = map(int, lines[304:309])
            hosp_ambulances = zip(hosp_ambulances, range(5))
            hosp_ambulances.sort(key = lambda x: int(x[0]))
                        
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
            
            
            means = [(49,56),(63,47),(48,53),(67,50),(31,49)]
            
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
                h = [cluster_distances[i][1],cluster_distances[i][2]]
                sort_wrt(h)
                no = int(round(300 * hosp_ambulances[i][0] / sum(map(lambda x : x[0], hosp_ambulances))))
                hospitals.append(Hospital((h[0], h[1]), patients[0:no-1],  
                                           hosp_ambulances[i][0], hosp_ambulances[i][1]))
                del patients[0:no-1]
            
            total_saves = 0
            
            for hospital in hospitals:
                hospital.assign_patients()
                for ambulance in hospital.ambulances:
                    routes = ambulance.get_route(timefactor)
                    if not routes:
                        continue
                    for route in routes:
                        for patient in route:
                            if(isinstance(patient,Patient)):
                                if patient.saved:
                                    total_saves += 1
                
            if total_saves > total_score:
                total_score = total_saves
                best_j = float(meansscale)
                best_time = timefactor 
                print_result(hospitals, "team_output.txt")
                
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

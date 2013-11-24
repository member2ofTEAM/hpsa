"""
Endlessly bouncing ball - demonstrates animation using Python and TKinter
"""
import time
import random
import math
import pdb
from sets import Set
import socket
import re

import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

play_as = sys.argv[1]
port_nr = int(sys.argv[2])
print play_as
print port_nr

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", port_nr))

team_name = "TEAM"
maxlen = 1
eom = "\n"

def serversaid(msg):
    print("Server: %s"%msg[:80])
def isaid(msg):
    print("Client: %s"%msg[:80])
def makemove(socket,pid,x,y):
    sendsocket(socket,"(%d,%d,%d)"%(pid,x,y))
def distance_squared(x0, y0, x1, y1):
    return (x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1)

def readsocket(sock,timeout=0):
    inpData=''
    while True:
        chunk = sock.recv(maxlen)
        if not chunk: break
        if chunk == '':
            raise RuntimeError("socket connection broken")
        inpData = inpData + chunk
        if eom in inpData:
            break
    inpData=inpData[:-1]
    return inpData
  
def sendsocket(sock,msg):
    msg += eom
    totalsent=0
    MSGLEN = len(msg) 
    while totalsent < MSGLEN:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    isaid(msg)

#Team Name?
in_msg = readsocket(s)
#Response
if("Team Name?" in in_msg):
  sendsocket(s,team_name+eom)
#N M
in_msg = readsocket(s)
in_msg = in_msg.split(" ")
ticks_to_set = int(in_msg[0])
max_walls = int(in_msg[1])
'''
#Walls
in_msg = readsocket(s)
#no walls on board
in_msg = readsocket(s)
no_walls_build = int(in_msg)
#walls CHECK WHETHER IT WORKS
walls = []
for i in range(no_walls_build):
  in_msg = readsocket(s)
  in_msg = in_msg.split(" ")
  walls.append((int(in_msg[0]),in_msg[1]))
#Moves to next wall build
in_msg = readsocket(s)
in_msg = readsocket(s)
set_count = ticks_to_set - int(in_msg)
#Hunter
#probably have to change dictionary
in_msg = readsocket(s)
in_msg = in_msg.split(" ")
hunter_direction = in_msg[1]
hunter_pos = in_msg[2]
t = tuple(int(v) for v in re.findall("[0-9]+", hunter_pos))
h_x = t[0]
h_y = t[1]
#Prey
in_msg = readsocket(s)
in_msg = in_msg.split(" ")
prey_pos = in_msg[1]
t = tuple(int(v) for v in re.findall("[0-9]+", prey_pos))
x_prey = t[0]
y_prey = t[1]
#Remaining Time
time_remain = float(readsocket(s))
print h_x, h_y
print x_prey,y_prey
print time_remain
'''

tick = 0

h_x = 0
h_y = 0
x_prey = 330
y_prey = 200

# Initial coordinates
x0 = 0
y0 = 0

ball_diameter = 30

# Get TKinter ready to go
from Tkinter import *
window = Tk()
canvas = Canvas(window, width=500, height=500, bg='white')
canvas.pack()

heatmap = [[100 for value in range(500)] for value in range(500)] 

hunter_predict_x = 0
hunter_predict_y = 0

predict_steps = 200

last_hunter_x = 0
last_hunter_y = 0

# The velocity, or distance moved per time step
vx = 1    # x velocity
vy = 1    # y velocity

# Boundaries
x_min = -1
y_min = -1
x_max = 500
y_max = 500

wall_vertical_out = [(-4,(x_min,y_min),(x_min,y_max)),(-3,(x_max,y_min),(x_max,y_max))]
wall_horizontal_out = [(-2,(x_min,y_min),(x_max,y_min)),(-1,(x_min,y_max),(x_max,y_max))]

wall_vertical = {'-4': x_min, '-3':x_max}
wall_horizontal = {'-2':y_min, '-1':y_max}

# Moves
prey_moves = {(0,-1):'NN',(1,-1):'NE',(1,0):'EE',(1,1):'SE',(0,1):'SS',(-1,1):'SW',(-1,0):'WW',(-1,-1):'NW',(0,0):'ZZ'}
hunter_moves = prey_moves.values() + [move+'h' for move in prey_moves.values()] + [move+'v' for move in prey_moves.values()] + ['r'+value for value in wall_horizontal.keys()+wall_vertical.keys() if int(value)>=0]

prey_queue = [(0,0)]
prey_move = (0,0)

can_set = 1

pause = -1

id = 0

max_tick = 0
all_prey_moves = []

canvas.create_rectangle(x_prey-2, y_prey-2, x_prey + 2, y_prey + 2, fill = "blue", tag = 'prey')

    
def vertical_check(pos_x):
    if pos_x >= x_max or pos_x <= x_min or pos_x in wall_vertical.values():
        return True
    
def horizontal_check(pos_y):
    if pos_y >= y_max or pos_y <= y_min or pos_y in wall_horizontal.values():
        return True
        
def l1d((x, y), mid_x, mid_y):
    return max(abs(mid_x - x), abs(mid_y - y))    
    
def calculate_heat(steps,hunter_vx,hunter_vy,hunter_x,hunter_y,heatmap):   
    pot_x = hunter_x
    pot_y = hunter_y
    
    pot_vx = hunter_vx
    pot_vy = hunter_vy
        
    
    pos = ((x_prey,y_prey),0)
    pos_set = [pos]
    visited = []
    visited.append(pos[0])
    heatmap[pos[0][0]][pos[0][1]] = pos[1]
    temp_moves = [move for move in prey_moves.keys() if not move == (0,0)]
        
    # Distance in which Prey can move within 30 steps                    
    while pos_set:
        pos = pos_set.pop(0)
                
        for move in temp_moves:
            mx = pos[0][0]+move[0]
            my = pos[0][1]+move[1]
            if (mx,my) not in visited and pos[1]+2<=30:
                if not(vertical_check(mx)):
                    if not(horizontal_check(my)):
                        pos_set.append(((mx,my),pos[1]+2))
                        visited.append((mx,my))
                        heatmap[mx][my] = pos[1]+2
                        
    
    # Gravity
    mid_x = 0
    mid_y = 0
    
    visited = []
    
    h_walls = wall_horizontal.values()
    h_walls.sort()
    for (y_i, y_j) in zip(h_walls, h_walls[1:]):
        if y_i < y_prey and y_prey < y_j:
            v_walls = wall_vertical.values()
            v_walls.sort()
            for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                if x_i < x_prey and x_prey < x_j:
                    mid_x = x_i+(x_j-x_i)/2
                    mid_y = y_i+(y_j-y_i)/2
    
    
                                        
    init = ((mid_x,mid_y),0)
        
    l = range(500)
    
    for i in range(500):
        for j in range(500):
            heatmap[i][j] = heatmap[i][j] + 1000*(l1d((i, j), mid_x, mid_y))
          
    # Prediction of Hunter Moves            
    for i in range(steps):        
        canvas.delete('predict'+str(i))
    for i in range(steps): 
        print i
        minx = 500
        miny = 500
        maxx = 0
        maxy = 0       
        for k in range(10):
            for l in range(10):
                offset_x = pot_x+k-4
                offset_y = pot_y+l-4                
                
                if not(vertical_check(offset_x)):
                    if not(vertical_check(offset_y)):
                        heatmap[offset_x][offset_y] += 50 + steps-(int(i)/2)
                        if offset_x > maxx:
                            maxx = offset_x
                        if offset_y > maxy:
                            maxy = offset_y
                        if offset_x < minx:
                            minx = offset_x
                        if offset_y < miny:
                            miny = offset_y
    
        canvas.create_rectangle(minx, miny, maxx, maxy, fill = "yellow", tag = 'predict'+str(i))
        canvas.update() 
        pot_x = pot_x + pot_vx
        pot_y = pot_y + pot_vy
        # If a boundary has been crossed, reverse the direction
        if vertical_check(pot_x):
            pot_vx = pot_vx*-1
    
        if horizontal_check(pot_y):
            pot_vy = pot_vy*-1 
            
    
def euclidean_distance(pos1,pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)   
            
            
def find_safest_path(pos):
    print "current_pos is" + str((x_prey,y_prey))
    print "Pos is: " + str(pos)
    queue = []
    temp_queue = []
    temp_moves = [move for move in prey_moves.keys() if not move == (0,0)]
    checked = []
    
    if (x_prey,y_prey)==pos:
        queue.append((0,0))
        return queue
    
    while (x_prey,y_prey)!=pos:
        temp_queue = []
        for move in temp_moves:
            mx = pos[0]+move[0]
            my = pos[1]+move[1]
            
            if not (mx,my) in checked:
                if not(vertical_check(mx)):
                    if not(horizontal_check(my)):
                        temp_queue.append((heatmap[mx][my]+100*euclidean_distance((mx,my),(x_prey,y_prey)),(move[0],move[1])))
                        checked.append((mx,my))
        temp_queue.sort()
        print temp_queue[0]
        print pos
        pos = (pos[0]+temp_queue[0][1][0],pos[1]+temp_queue[0][1][1])
        queue.append((temp_queue[0][1][0],temp_queue[0][1][1]))
        
    
    queue.sort(reverse=True)
    return queue
        

def handler(event):
    global pause
    
    if event.char in('p'):
        pause = pause * -1
        
def parse_wall(entries):
  canvas.delete("all")
  for entry in entries:
    wall = [int(v) for v in re.findall("[0-9]+", entry[1])]
    if(wall[1]==wall[3]):
      hw = (entry[0],(wall[0],wall[1]),(wall[2],wall[3]))
      wall_horizontal_out.append(hw)
      wall_horizontal[entry[0]]=wall[1]
      canvas.create_line(wall[0], wall[1], wall[2], wall[3], fill="black")
      canvas.update()
      print wall_horizontal
    if(wall[0]==wall[2]):
      vw = (entry[0],(wall[0],wall[1]),(wall[2],wall[3]))
      wall_vertical_out.append(vw)
      wall_vertical[entry[0]]=wall[0]
      canvas.create_line(wall[0], wall[1], wall[2], wall[3], fill="black")
      canvas.update()
      print wall_vertical

window.bind('<Key>', handler)

tick = 0
# For each timestep
while(1):
    #Walls
    in_msg = readsocket(s)
    #no walls on board
    in_msg = readsocket(s)
    no_walls_build = int(in_msg)
    print no_walls_build
    #walls CHECK WHETHER IT WORKS
    walls = []
    for i in range(no_walls_build):
      in_msg = readsocket(s)
      in_msg = in_msg.split(" ")
      walls.append((int(in_msg[0]),in_msg[1]))
      print walls
    #Moves to next wall build
    in_msg = readsocket(s)
    in_msg = readsocket(s)
    set_count = ticks_to_set - int(in_msg)
    if set_count>=ticks_to_set:
      can_set = True
    else:
      can_set = False
    #Hunter
    #probably have to change dictionary
    in_msg = readsocket(s)
    in_msg = in_msg.split(" ")
    hunter_direction = in_msg[1]
    hunter_pos = in_msg[2]
    t = tuple(int(v) for v in re.findall("[0-9]+", hunter_pos))
    h_x = t[0]
    h_y = t[1]
    #Prey
    in_msg = readsocket(s)
    in_msg = in_msg.split(" ")
    prey_pos = in_msg[1]
    t = tuple(int(v) for v in re.findall("[0-9]+", prey_pos))
    x_prey = t[0]
    y_prey = t[1]
    #Remaining Time
    time_remain = float(readsocket(s))
    print h_x, h_y
    print x_prey,y_prey
    print time_remain
    
    wall_vertical_out = [(-4,(x_min,y_min),(x_min,y_max)),(-3,(x_max,y_min),(x_max,y_max))]
    wall_horizontal_out = [(-2,(x_min,y_min),(x_max,y_min)),(-1,(x_min,y_max),(x_max,y_max))]

    wall_vertical = {'-4': x_min, '-3':x_max}
    wall_horizontal = {'-2':y_min, '-1':y_max}
    
    parse_wall(walls)
    
    
    canvas.create_rectangle(h_x-2, h_y-2, h_x+2, h_y+2, fill="red", tag='blueball')
    
    if play_as == 'H':
        if can_set and len(wall_horizontal.keys()+wall_vertical.keys())<max_walls+4:
	    print can_set
	    print len(wall_horizontal.keys()+wall_vertical.keys())
        
        #build vertical wall
	    if(h_x==100)and(x_prey!=100 and y_prey != h_y):
	      h_walls = wall_horizontal.values()
	      h_walls.sort()
	      for (y_i, y_j) in zip(h_walls, h_walls[1:]):
		  if y_i < h_y and h_y < y_j and y_i < y_prey and y_prey < y_j:
		      v_walls = wall_vertical.values()
		      print "Test"
		      v_walls.sort()
		      for (x_i, x_j) in zip(v_walls, v_walls[1:]):
			  if x_i < h_x and x_i < x_prey and h_x < x_j and x_prey < x_j:
			      for i in range(len(wall_vertical.keys()+wall_horizontal.keys())):
				  if str(i) in wall_vertical.keys()+wall_horizontal.keys():
				      continue
				  else:
				      id = i
				      break
			      wall_vertical[str(id)] = h_x
			      print "Test2"
			      wall_vertical_out.append((id, (h_x, y_i+1),( h_x, y_j-1)))       
			      print (hunter_direction+"w"+"("+str(h_x)+","+str(y_i+1)+")"+","+"("+str(h_x)+","+str(y_j-1)+")"+'\n')
			      sendsocket(s,(hunter_direction+"w"+"("+str(h_x)+","+str(y_i+1)+")"+","+"("+str(h_x)+","+str(y_j-1)+")"+'\n'))
			      canvas.create_line(h_x, y_i, h_x, y_j, fill="black")
			      canvas.update()
			      can_set = 0  
			      
	    elif(h_y==200)and(x_prey!=200 and y_prey != h_y):
                h_walls = wall_horizontal.values()
                h_walls.sort()
                for (y_i, y_j) in zip(h_walls, h_walls[1:]):
                    if y_i < h_y and h_y < y_j and y_i < y_prey and y_prey < y_j:
                        v_walls = wall_vertical.values()
                        v_walls.sort()
                        for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                            if x_i < h_x and x_i < x_prey and h_x < x_j and x_prey < x_j:
                                for i in range(len(wall_vertical.keys()+wall_horizontal.keys())):
                                    if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                                        continue
                                    else:
                                        id = i
                                        break
                                wall_horizontal[str(id)] = h_y
                                wall_horizontal_out.append((id, (x_i+1, h_y),( x_j-1, h_y)))
                                print (hunter_direction+"w"+"("+str(x_i+1)+","+str(h_y)+")"+","+"("+str(x_j-1)+","+str(h_y)+")"+'\n')
                                sendsocket(s,(hunter_direction+"w"+"("+str(x_i+1)+","+str(h_y)+")"+","+"("+str(x_j-1)+","+str(h_y)+")"+'\n'))
                                canvas.create_line(x_i, h_y, x_j, h_y, fill="black")
                                canvas.update()
                                can_set = 0    
            elif(((x_prey-h_x)<=6 and (x_prey-h_x)>=2 and prey_moves[(vx,vy)] in ('NE','EE','SE'))) or (((h_x-x_prey)<=6 and (h_x-x_prey)>=2 and prey_moves[(vx,vy)] in ('NW','WW','SW'))):
                h_walls = wall_horizontal.values()
                h_walls.sort()
                for (y_i, y_j) in zip(h_walls, h_walls[1:]):
                    if y_i < h_y and h_y < y_j and y_i < y_prey and y_prey < y_j:
                        v_walls = wall_vertical.values()
                        print "Test"
                        v_walls.sort()
                        for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                            if x_i < h_x and x_i < x_prey and h_x < x_j and x_prey < x_j:
                                for i in range(len(wall_vertical.keys()+wall_horizontal.keys())):
                                    if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                                        continue
                                    else:
                                        id = i
                                        break
                                wall_vertical[str(id)] = h_x
                                print "Test2"
                                wall_vertical_out.append((id, (h_x, y_i+1),( h_x, y_j-1)))       
                                print (hunter_direction+"w"+"("+str(h_x)+","+str(y_i+1)+")"+","+"("+str(h_x)+","+str(y_j-1)+")"+'\n')
                                sendsocket(s,(hunter_direction+"w"+"("+str(h_x)+","+str(y_i+1)+")"+","+"("+str(h_x)+","+str(y_j-1)+")"+'\n'))
                                canvas.create_line(h_x, y_i, h_x, y_j, fill="black")
                                canvas.update()
                                can_set = 0                           
                                
            #build horizontal wall
            elif(((h_y-y_prey)<=6 and (h_y-y_prey)>=2 and prey_moves[(vx,vy)] in ('NE','NN','NW'))) or (((h_y-y_prey)>=-6 and (h_y-y_prey)<=-2 and prey_moves[(vx,vy)] in ('SE','SS','SW'))):
                h_walls = wall_horizontal.values()
                h_walls.sort()
                for (y_i, y_j) in zip(h_walls, h_walls[1:]):
                    if y_i < h_y and h_y < y_j and y_i < y_prey and y_prey < y_j:
                        v_walls = wall_vertical.values()
                        v_walls.sort()
                        for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                            if x_i < h_x and x_i < x_prey and h_x < x_j and x_prey < x_j:
                                for i in range(len(wall_vertical.keys()+wall_horizontal.keys())):
                                    if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                                        continue
                                    else:
                                        id = i
                                        break
                                wall_horizontal[str(id)] = h_y
                                wall_horizontal_out.append((id, (x_i+1, h_y),( x_j-1, h_y)))
                                print (hunter_direction+"w"+"("+str(x_i+1)+","+str(h_y)+")"+","+"("+str(x_j-1)+","+str(h_y)+")"+'\n')
                                sendsocket(s,(hunter_direction+"w"+"("+str(x_i+1)+","+str(h_y)+")"+","+"("+str(x_j-1)+","+str(h_y)+")"+'\n'))
                                canvas.create_line(x_i, h_y, x_j, h_y, fill="black")
                                canvas.update()
                                can_set = 0
            else:
	      print 45678987654
	      sendsocket(s,hunter_direction+'\n')
	else:
	  print 45678987654
	  sendsocket(s,hunter_direction+'\n')
    else:                        
	#if not input_text:
	steps = random.randint(85, 115)
	if len(prey_queue)==0:
	    prey_queue.append(random.choice(prey_moves.keys()))
	    prey_queue = prey_queue*steps        
    
	if vertical_check(x_prey):
	    prey_move = (prey_move[0]*-1,prey_move[1])
	    prey_queue = []
	    prey_queue.append(prey_move)
	    prey_queue = prey_queue*steps       
    
	if horizontal_check(y_prey):
	    prey_move = (prey_move[0],prey_move[1]*-1)
	    prey_queue = []
	    prey_queue.append(prey_move)
	    prey_queue = prey_queue*steps
	    
	#index = int(tick)/2
	#print index
	prey_move = prey_queue.pop()
	#prey_move = prey_queue_input[index]
	all_prey_moves.append((prey_move[0], prey_move[1]))
	x_prey = x_prey + prey_move[0]
	#x_prey = prey_move[0]
	y_prey = y_prey + prey_move[1]
	
	sendsocket(s,(prey_moves[prey_move[0],prey_move[1]])+'\n')

    # New coordinate equals old coordinate plus distance-per-timestep
    
    canvas.delete('prey')
    canvas.create_rectangle(x_prey-5, y_prey-5, x_prey+5, y_prey+5, fill = "blue", tag = 'prey')
    canvas.update() 
    
    h_x = h_x + vx
    h_y = h_y + vy

    # If a boundary has been crossed, reverse the direction
    if vertical_check(h_x):
        vx = vx*-1

    if horizontal_check(h_y):
        vy = vy*-1

    

    canvas.update()

    # Pause for 0.05 seconds, then delete the image
    time.sleep(0.01)
    canvas.delete('blueball')
    tick += 1

    if set_count >= ticks_to_set:
        can_set = 1
    '''    
    if x_prey in range(h_x - 4, h_x + 5) and y_prey in range(h_y - 4, h_y + 5):
        print "Hinter wina witha " + str(tick) + " stepsaaa"
        quit()
    '''

#f.close()

# I don't know what this does but the script won't run without it.
window.mainloop()

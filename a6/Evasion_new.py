"""
Endlessly bouncing ball - demonstrates animation using Python and TKinter
"""
import time
import random
import math
import pdb
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

# Initial coordinates
x0 = 0
y0 = 0

ball_diameter = 30

# Get TKinter ready to go
from Tkinter import *
window = Tk()
canvas = Canvas(window, width=500, height=500, bg='white')
canvas.pack()

hunter_predict_x = 0
hunter_predict_y = 0

predict_steps = 200

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
hunter_moves = (prey_moves.values() + [move+'h' for move in prey_moves.values()]
               + [move+'v' for move in prey_moves.values()] 
               + ['r'+value for value in wall_horizontal.keys()+wall_vertical.keys() if int(value)>=0])

prey_queue = 30*[(-1,0)]
reey_move = (0,0)

h_x = x0
h_y = y0

x_prey = 320
y_prey = 200

can_set = 1

set_count = 30

pause = -1

ticks_to_set = 30
max_walls = 15
            
id = 0

canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
canvas.create_rectangle(h_x, h_y, h_x+4, h_y+4, fill="red", tag='blueball')
    
def vertical_check(pos_x):
    return pos_x in wall_vertical.values()
    
def horizontal_check(pos_y):
    return pos_y in wall_horizontal.values()
    
#Returns bounds on x and y
def prey_update_box():
    h_walls = wall_horizontal.values()
    h_walls.sort()
    for (y_i, y_j) in zip(h_walls, h_walls[1:]):
        if y_i < y_prey and y_prey < y_j:
            v_walls = wall_vertical.values()
            v_walls.sort()
            for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                if x_i < x_prey and x_prey < x_j:
                    return ((x_i, x_j), (y_i, y_j))

prey_boundary = prey_update_box()

def prey_area_box():
    return (abs(prey_boundary[0][0] - prey_boundary[0][1]) * 
            abs(prey_boundary[1][0] - prey_boundary[1][1]))

def prey_area_longated():
    return (abs(prey_boundary[0][0] - prey_boundary[0][1])/abs(prey_boundary[1][0] - prey_boundary[1][1]) > 5
         or abs(prey_boundary[1][0] - prey_boundary[1][1])/abs(prey_boundary[0][0] - prey_boundary[0][1]) > 5)


def hunter_update_box():
    #pdb.set_trace()
    h_walls = wall_horizontal.values()
    h_walls.sort()
    for (y_i, y_j) in zip(h_walls, h_walls[1:]):
        if y_i <= h_y and h_y < y_j:
            v_walls = wall_vertical.values()
            v_walls.sort()
            for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                if x_i <= h_x and h_x < x_j:
                    return ((x_i, x_j), (y_i, y_j))

hunter_boundary = hunter_update_box()

def hunter_pos_in_box(pos):
    return (hunter_boundary[0][0] < pos[0] and
            hunter_boundary[0][1] > pos[0] and
            hunter_boundary[1][0] < pos[1] and
            hunter_boundary[1][1] > pos[1])


def prey_pos_in_box(pos):
    return (prey_boundary[0][0] < pos[0] and
            prey_boundary[0][1] > pos[0] and
            prey_boundary[1][0] < pos[1] and
            prey_boundary[1][1] > pos[1])

img = PhotoImage(width=500, height=500)
canvas.create_image((250, 250), image=img, state="normal")

PREY_QSIZE = 30
HUNTER_PSIZE = 120
MAX_HEAT = 708

def distance(pos1,pos2):
    return math.sqrt(abs(pos1[0]-pos2[0])**2 + abs(pos1[1]-pos2[1])**2)

def draw_heat_line(s_x, s_y, e_x, e_y, heatmap):
    if s_x == e_x:
        if s_y <= e_y:
            for i in range(e_y, s_y + 1):
                heatmap[s_x][i] = MAX_HEAT
        if e_y < s_y:
            for i in range(s_y, e_y - 1, -1):
                heatmap[s_x][i] = MAX_HEAT
    if s_y == e_y:
        if s_x <= e_x:
            for i in range(e_x, s_x + 1):
                heatmap[i][s_x] = MAX_HEAT
        if e_x < s_x:
            for i in range(s_x, e_x - 1, -1):
                heatmap[i][s_x] = MAX_HEAT

def calculate_heat(steps, pot_vx, pot_vy, pot_x, pot_y, heatmap):
    # Prediction of Hunter Moves            
    (oh_x, oh_y) = (pot_x, pot_y)
    hunter_steps = []
    lhp = 120
    if prey_area_box() < 15000:
        lhp = 85 
    if prey_area_box() < 4000:
        lhp = 40
    for i in range(min(HUNTER_PSIZE, lhp)):
        hunter_steps.append((pot_x, pot_y))
        if vertical_check(pot_x + pot_vx):
            pot_vx = pot_vx*-1
        if horizontal_check(pot_y + pot_vy):
            pot_vy = pot_vy*-1
        if vertical_check(h_x + vx):
            pot_vx = 0
        if horizontal_check(h_y + vy):
            pot_vy = 0
        (pot_x, pot_y) = (pot_x + pot_vx, pot_y + pot_vy)

    if prey_area_longated():
        for i in range(x_prey - PREY_QSIZE - 1, x_prey + PREY_QSIZE + 1):
            for j in range(y_prey - PREY_QSIZE - 1, y_prey + PREY_QSIZE + 1):
                heatmap[i][j] = MAX_HEAT - distance(hunter_steps[0], (i, j))
    else:
        for i in range(x_prey - PREY_QSIZE - 1, x_prey + PREY_QSIZE + 1):
            for j in range(y_prey - PREY_QSIZE - 1, y_prey + PREY_QSIZE + 1):
                heatmap[i][j] = distance((i, j), (oh_x, oh_y))
    
        for (x, y) in hunter_steps[::-1]:
            for i in range(x - 10, x + 10):
                for j in range(y - 10, y + 10):
                    if distance((i, j), (x, y)) < 10 and hunter_pos_in_box((i, j)):
                        heatmap[i][j] = max((142 - 0.5*distance(hunter_steps[0], (i, j)))/
                                             142 * (MAX_HEAT - distance((x, y), 
                                        (i, j))), heatmap[i][j])
    for (id, (s_x, s_y), (e_x, e_y)) in wall_vertical_out:
         draw_heat_line(s_x, s_y, e_x, e_y, heatmap)

    for (id, (s_x, s_y), (e_x, e_y)) in wall_horizontal_out:
         draw_heat_line(s_x, s_y, e_x, e_y, heatmap)

#    for i in range(500):#x_prey - 100, x_prey + 100):
#        for j in range(500):#y_prey - 200, y_prey + 100):
#            img.put(str('#%02x%02x%02x' % ((255 * int(heatmap[i][j]))/MAX_HEAT, 0, 0)), (i,j))
    canvas.update()  

heatmap = [[0 for value in range(500)] for value in range(500)] 
calculate_heat(predict_steps,vx,vy,h_x,h_y,heatmap)
   
#Return coordinates of minimum entry in heatmap
def find_safest_path(prey_queue):
    start = (x_prey, y_prey)
    for trash in range(PREY_QSIZE):
        #By default the prey doesn't move
        best_next = [MAX_HEAT, (0, 0)]
        for move in prey_moves.keys():
            maybe_next = (start[0] + move[0], start[1] + move[1])
            if prey_pos_in_box(maybe_next):
               (mx, my) = maybe_next
               score = heatmap[mx][my]
               if score < best_next[0]:
                   best_next[0] = score
                   best_next[1] = move

        move = best_next[1]
        start = (start[0] + move[0], start[1] + move[1])
        prey_queue.append(move)

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
    #Read from Socket
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
    print in_msg
    in_msg = readsocket(s)
    print in_msg
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
    
    built = False
    removed = False
    
    if play_as == 'H':
      #Build wall 
      if can_set and len(wall_horizontal.keys()+wall_vertical.keys())<max_walls+4:
	  print len(wall_horizontal.keys()+wall_vertical.keys())
	  print can_set
	  
	  #build vertical wall
	  if (prey_pos_in_box((h_x, h_y)) and abs(h_x + vx - x_prey) <= 2 and (math.copysign(1,vx)!=math.copysign(1,(h_x - x_prey))) and h_x != x_prey):
	    id = max(map(lambda x: int(x), wall_vertical.keys() + wall_horizontal.keys())) + 1
	    wall_vertical[str(id)] = h_x
	    prey_boundary = prey_update_box()
	    hunter_boundary = hunter_update_box()
	    (y_i, y_j) = hunter_boundary[1]
	    wall_vertical_out.append((id, (h_x, y_i+1),( h_x, y_j-1)))
	    sendsocket(s,(hunter_direction+"w"+"("+str(h_x)+","+str(y_i+1)+")"+","+"("+str(h_x)+","+str(y_j-1)+")"+'\n'))
	    canvas.create_line(h_x, y_i, h_x, y_j, fill="black")
	    canvas.update()
	    can_set = 0
	    set_count = 0                           
	    del prey_queue[:]
	    built = True
			      
	  #build horizontal wall
	  elif (prey_pos_in_box((h_x, h_y)) and abs(h_y + vy - y_prey)<=2 and (math.copysign(1,vy)!=math.copysign(1,(h_y - y_prey))) and h_y != y_prey):
	    id = max(map(lambda x: int(x), wall_vertical.keys() + wall_horizontal.keys())) + 1
	    wall_horizontal[str(id)] = h_y
	    prey_boundary = prey_update_box()
	    hunter_boundary = hunter_update_box()
	    (x_i, x_j) = hunter_boundary[0]
	    wall_horizontal_out.append((id, (x_i+1, h_y),(x_j-1, h_y)))
	    sendsocket(s,(hunter_direction+"w"+"("+str(x_i+1)+","+str(h_y)+")"+","+"("+str(x_j-1)+","+str(h_y)+")"+'\n'))
	    canvas.create_line(x_i, h_y, x_j, h_y, fill="black")
	    canvas.update()
	    can_set = 0
	    set_count = 0
	    del prey_queue[:]
	    built = True
	  '''  
	  elif len(wall_horizontal.keys()+wall_vertical.keys()) > 4:
	    removable_walls = [wall for wall in (wall_vertical_out+wall_horizontal_out) if wall[0]>=0]
	    if prey_boundary == hunter_boundary:
	      wall_to_remove = (-2,-2)
	      for wall in removable_walls:
		if (not(wall[1][0] == hunter_boundary[0][0] and wall[1][1] == hunter_boundary[0][1])
		and(not(wall[1][0] == hunter_boundary[1][0] and wall[1][1] == hunter_boundary[1][1])):
		  wall_to_remove = wall[0]
		  sendsocket(s,(hunter_direction+"w"+str(wall_to_remove)+'\n'))
		  wall_horizontal = {key: value for key, value in wall_horizontal.items() if value != wall_to_remove}
		  wall_vertical = {key: value for key, value in wall_vertical.items() if value != wall_to_remove}
		  removed = True
	 '''	  
	  if not(built) and not(removed):
	    sendsocket(s,hunter_direction+'\n')
      else:
	sendsocket(s,hunter_direction+'\n')
    else:
      #Update prey   
	if not prey_queue: 
	    calculate_heat(predict_steps,vx,vy,h_x,h_y,heatmap)
	    find_safest_path(prey_queue)
	
	#There may be nothing more to do
	if prey_queue:
	    prey_move = prey_queue.pop(0)
	    x_prey = x_prey + prey_move[0]
	    y_prey = y_prey + prey_move[1]
	
	sendsocket(s,(prey_moves[prey_move[0],prey_move[1]])+'\n')
	  
    canvas.delete('prey')
    canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
    canvas.update()
       
    #Update hunter
    if vertical_check(h_x + vx):
        vx = vx*-1
    if horizontal_check(h_y + vy):
        vy = vy*-1
    if vertical_check(h_x + vx):
        vx = 0
    if horizontal_check(h_y + vy):
        vy = 0
    h_x = h_x + vx
    h_y = h_y + vy
    hunter_boundary = hunter_update_box()

    #Redraw
    canvas.delete('blueball')
    canvas.create_rectangle(h_x, h_y, h_x+4, h_y+4, fill="red", tag='blueball')
    canvas.update()
    
    #Increae ticks
    time.sleep(0.01)
    tick += 1
    set_count += 1
    if set_count >= ticks_to_set:
        can_set = 1
    
    #Check winning condition
    if x_prey in range(h_x - 4, h_x + 5) and y_prey in range(h_y - 4, h_y + 5):
        print "Hinter wina witha " + str(tick) + " stepsaaa"
        quit()

window.mainloop()

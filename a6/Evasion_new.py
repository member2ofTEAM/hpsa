"""
Endlessly bouncing ball - demonstrates animation using Python and TKinter
"""
import time
import random
import math
import pdb
from sets import Set


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
x_min = 0
y_min = 0
x_max = 499
y_max = 499

MAX_HEAT = 1000000

wall_vertical_out = [(-4,(x_min,y_min),(x_min,y_max)),(-3,(x_max,y_min),(x_max,y_max))]
wall_horizontal_out = [(-2,(x_min,y_min),(x_max,y_min)),(-1,(x_min,y_max),(x_max,y_max))]

wall_vertical = {'-4': x_min, '-3':x_max}
wall_horizontal = {'-2':y_min, '-1':y_max}

# Moves
prey_moves = {(0,1):'NN',(1,1):'NE',(1,0):'EE',(1,-1):'SE',(0,-1):'SS',(-1,-1):'SW',(-1,0):'WW',(-1,1):'NW',(0,0):'XX'}
hunter_moves = (prey_moves.values() + [move+'h' for move in prey_moves.values()]
               + [move+'v' for move in prey_moves.values()] 
               + ['r'+value for value in wall_horizontal.keys()+wall_vertical.keys() if int(value)>=0])

prey_queue = [(0,0)]
prey_move = (0,0)

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
    
def vertical_check(pos_x):
    return pos_x >= x_max or pos_x <= x_min or pos_x in wall_vertical.values()
    
def horizontal_check(pos_y):
    return pos_y >= y_max or pos_y <= y_min or pos_y in wall_horizontal.values()
        
def l1d((x, y), mid_x, mid_y):
    return max(abs(mid_x - x), abs(mid_y - y))   
    
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
                    prey_boundary = ((x_i, x_j), (y_i, y_j))

prey_boundary = ((0, 0), (0, 0))
prey_update_box()

def hunter_update_box():
    h_walls = wall_horizontal.values()
    h_walls.sort()
    for (y_i, y_j) in zip(h_walls, h_walls[1:]):
        if y_i < y_prey and y_prey < y_j:
            v_walls = wall_vertical.values()
            v_walls.sort()
            for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                if x_i < x_prey and x_prey < x_j:
                    hunter_boundary = ((x_i, x_j), (y_i, y_j))

hunter_boundary = ((0, 0), (0, 0))
hunter_update_box()

def prey_pos_in_box(pos):
    return (prey_boundary[0][0] < pos[0] and
            prey_boundary[0][1] > pos[0] and
            prey_boundary[1][0] < pos[1] and
            prey_boundary[1][1] > pos[1])

def calculate_heat(steps,hunter_vx,hunter_vy,hunter_x,hunter_y,heatmap):   
    pot_x = hunter_x
    pot_y = hunter_y
    
    pot_vx = hunter_vx
    pot_vy = hunter_vy
        
#    pdb.set_trace()
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
            if (((mx,my) not in visited) and (pos[1]+2<=30) 
                    and not(vertical_check(mx) or horizontal_check(my))):
                        pos_set.append(((mx,my),pos[1]+2))
                        visited.append((mx,my))
                        heatmap[mx][my] = pos[1]+2
                        
    
    # Gravity
    mid_x = 0
    mid_y = 0
    ((x_i, x_j), (y_i, y_j)) = prey_boundary 
    mid_x = x_i+(x_j-x_i)/2
    mid_y = y_i+(y_j-y_i)/2
    
    init = ((mid_x,mid_y),0)
        
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
            
            
def find_safest_path(pos, prey_queue):
    print "current_pos is" + str((x_prey,y_prey))
    print "Pos is: " + str(pos)
    del  prey_queue[:]
    temp_moves = [move for move in prey_moves.keys() if not move == (0,0)]
    checked = []
    
    if (x_prey,y_prey)==pos:
        prey_queue.append((0,0))
    else:
        while (x_prey,y_prey)!=pos:
            temp_queue = []
            for move in temp_moves:
                mx = pos[0]+move[0]
                my = pos[1]+move[1]
                
                if not (mx,my) in checked:
                    if not(vertical_check(mx)):
                        if not(horizontal_check(my)):
                            temp_queue.append((heatmap[mx][my]+100*euclidean_distance((mx,my),
                                              (x_prey,y_prey)),(move[0],move[1])))
                            checked.append((mx,my))
            temp_queue.sort()
            #The prey may be cornered and can't move anymore
            if not temp_queue:
                break
            print temp_queue[0]
            print pos
            pos = (pos[0]+temp_queue[0][1][0],pos[1]+temp_queue[0][1][1])
            prey_queue.append((temp_queue[0][1][0],temp_queue[0][1][1]))
        prey_queue.sort(reverse=True)

def handler(event):
    global pause
    
    if event.char in('p'):
        pause = pause * -1
        

window.bind('<Key>', handler)

tick = 0
# For each timestep
while(1):
    if(pause==1):
        raw_input('pressa di pi')
        pause = pause *-1
        continue
    canvas.create_rectangle(h_x, h_y, h_x+4, h_y+4, fill="red", tag='blueball')
    
    if can_set and len(wall_horizontal.keys()+wall_vertical.keys())<max_walls:
    
    #build vertical wall
        if ((((x_prey-h_x)<=6 and (x_prey-h_x)>=2 and prey_moves[(vx,vy)] in ('NE','EE','SE'))) 
           or (((h_x-x_prey)<=6 and (h_x-x_prey)>=2 and prey_moves[(vx,vy)] in ('NW','WW','SW')))
           and prey_pos_in_box((h_x, h_y))):

           for i in range(len(wall_vertical.keys()+wall_horizontal.keys())):
               if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                   continue
               else:
                   id = i
                   break
           wall_vertical[str(id)] = h_x
           (y_i, y_j) = hunter_boundary[1]
           wall_vertical_out.append((id, (h_x, y_i),( h_x, y_j)))
           prey_update_box()
           canvas.create_line(h_x, y_i, h_x, y_j, fill="black")
           canvas.update()
           can_set = 0
           set_count = 0                           
                            
        #build horizontal wall
        if ((((y_prey-h_y)<=6 and (y_prey-h_y)>=2 and prey_moves[(vx,vy)] in ('NE','NN','NW'))) 
           or (((y_prey-h_y)>=-6 and (y_prey-h_y)<=-2 and prey_moves[(vx,vy)] in ('SE','SS','SW')))
           and prey_pos_in_box((h_x, h_y))):

           for i in range(len(wall_vertical.keys()+wall_horizontal.keys())):
               if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                   continue
               else:
                   id = i
                   break
           wall_horizontal[str(id)] = h_y
           (x_i, x_j) = hunter_boundary[0]
           wall_horizontal_out.append((id, (x_i, h_y),( x_j, h_y))) 
           prey_update_box()
           canvas.create_line(x_i, h_y, x_j, h_y, fill="black")
           canvas.update()
           can_set = 0
           set_count = 0
             
                  
    if tick % 2 and tick > 1:
        
        if (len(prey_queue) == 1 
            or hunter_predict_x != last_predict_x 
            or hunter_predict_y != last_predict_y):
        
            last_predict_x = hunter_predict_x
            last_predict_y = hunter_predict_y
            hunter_predict_x = vx
            hunter_predict_y = vy
            heatmap = [[100 for value in range(500)] for value in range(500)] 
            
            calculate_heat(predict_steps,hunter_predict_x,hunter_predict_y,h_x,h_y,heatmap)
                            
            next_pos = (MAX_HEAT, (0, 0))
            for i in range(-15 + x_prey, 16 + x_prey):
                for j in range(-15 + y_prey, 16 + y_prey):
                    if prey_pos_in_box((i, j)):
                        if heatmap[i][j] < next_pos[0]:
                            next_pos[1] = (i, j)
                        
            last_hunter_x = h_x
            last_hunter_y = h_y 
            
            pos = next_pos[1]
            print pos
            
            canvas.delete('prey_pos')
            canvas.create_rectangle(pos[0]-5, pos[1]-5, pos[0]+5, pos[1]+5, fill = "green", tag = 'prey_pos')
            canvas.update() 
            
            find_safest_path(pos, prey_queue)
            print prey_queue
                    
        if prey_queue:
            prey_move = prey_queue.pop(0)
        
        x_hyp = x_prey + prey_move[0]
        y_hyp = y_prey + prey_move[1]
        
        if vertical_check(x_hyp) or horizontal_check(y_hyp):
            prey_queue = []
            prey_move = []
            for move in prey_moves.keys():
                x_hyp = x_prey + move[0]
                y_hyp = y_prey + move[1]
                if vertical_check(x_hyp) or vertical_check(y_hyp):
                    continue
                else:
                    prey_move.append((move[0],move[1]))

                    
            prey_move = random.choice(prey_move)
                

        x_prey = x_prey + prey_move[0]
        y_prey = y_prey + prey_move[1]
        canvas.delete('prey')
        canvas.create_rectangle(x_prey-2, y_prey-2, x_prey + 2, y_prey + 2, fill = "blue", tag = 'prey')
        canvas.update()
       
    # New coordinate equals old coordinate plus distance-per-timestep
    h_x = h_x + vx
    h_y = h_y + vy

    # If a boundary has been crossed, reverse the direction
    if vertical_check(h_x):
        vx = vx*-1

    if horizontal_check(h_y):
        vy = vy*-1

    hunter_update_box()

    canvas.update()
    # Pause for 0.05 seconds, then delete the image
    time.sleep(0.01)
    canvas.delete('blueball')
    tick += 1
    set_count += 1

    if set_count >= ticks_to_set:
        can_set = 1
        
    if x_prey in range(h_x - 4, h_x + 5) and y_prey in range(h_y - 4, h_y + 5):
        print "Hinter wina witha " + str(tick) + " stepsaaa"
        quit()

#f.close()

# I don't know what this does but the script won't run without it.
window.mainloop()

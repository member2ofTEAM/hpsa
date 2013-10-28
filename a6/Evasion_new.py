"""
Endlessly bouncing ball - demonstrates animation using Python and TKinter
"""
import time
import random
import math
import pdb

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
            
heatmap = [[0 for value in range(500)] for value in range(500)] 

id = 0

canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
canvas.create_rectangle(h_x, h_y, h_x+4, h_y+4, fill="red", tag='blueball')
    
def vertical_check(pos_x):
    return pos_x >= x_max or pos_x <= x_min or pos_x in wall_vertical.values()
    
def horizontal_check(pos_y):
    return pos_y >= y_max or pos_y <= y_min or pos_y in wall_horizontal.values()
        
def lmd((x, y), mid_x, mid_y):
    return max(abs(mid_x - x), abs(mid_y - y))   
    
#Returns bounds on x and y
def prey_update_box():
    h_walls = wall_horizontal.values()
    h_walls.sort()
    for (y_i, y_j) in zip(h_walls, h_walls[1:]):
        if y_i <= y_prey and y_prey < y_j:
            v_walls = wall_vertical.values()
            v_walls.sort()
            for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                if x_i <= x_prey and x_prey < x_j:
                    return ((x_i, x_j), (y_i, y_j))

prey_boundary = prey_update_box()

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

def calculate_heat(steps,hunter_vx,hunter_vy,hunter_x,hunter_y,heatmap):   
    pot_x = hunter_x
    pot_y = hunter_y
    pot_vx = hunter_vx
    pot_vy = hunter_vy
        
    # Distance in which Prey can move within 30 steps
    for i in range(-15 + x_prey, 16 + x_prey):
        for j in range(-15 + y_prey, 16 + y_prey):
             if prey_pos_in_box((i, j)):
                 heatmap[i][j] = lmd((i, j), x_prey, y_prey)
    
    # Gravity
    ((x_i, x_j), (y_i, y_j)) = prey_boundary 
    mid_x = x_i+(x_j-x_i)/2
    mid_y = y_i+(y_j-y_i)/2
    
    for i in range(500):
        for j in range(500):
            heatmap[i][j] = heatmap[i][j] + 1000*(lmd((i, j), mid_x, mid_y))
          
    # Prediction of Hunter Moves            
    for i in range(steps): 
        canvas.delete('predict'+str(i))
        for k in range(pot_x - 5, pot_x + 5):
            for l in range(pot_y - 5, pot_y + 5):
                if hunter_pos_in_box((k, l)):
                    heatmap[k][l] += 50 + steps-(int(i)/2)
    
        canvas.create_rectangle(pot_x, pot_y, pot_x + 4, pot_y + 4, fill = "yellow", tag = 'predict'+str(i))
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
    
#Return coordinates of minimum entry in heatmap
def min_heatmap():
    #THIS IS WRONG!
    best_e = (-1, -1)
    min_e = MAX_HEAT
    for row in range(len(heatmap)):
        for e in range(len(heatmap[row])):
            if min_e > heatmap[row][e]:
                min_e = e
                best_e = (row, e)
    return best_e

def find_safest_path(prey_queue):
    print "current_pos is" + str((x_prey,y_prey))
    del  prey_queue[:]
    start = (x_prey, y_prey)
    goal = min_heatmap()

    temp_moves = [move for move in prey_moves.keys() if not move == (0,0)]
    #pdb.set_trace()
    if start == goal:
        prey_queue.append((0,0))
    else:
        while start != goal:
            best_next = [MAX_HEAT, (-1, -1)]
            for move in temp_moves:
                maybe_next = (start[0] + move[0], start[1] + move[1])
                if prey_pos_in_box(maybe_next):
                   (mx, my) = maybe_next
                   score = heatmap[mx][my] + 10000*euclidean_distance(goal, maybe_next)
                   if score < best_next[0]:
                       best_next[0] = score
                       best_next[1] = move

            #The prey may be cornered and can't move anymore
            if best_next[1] == (-1, -1):
                break
            start = start + best_next[1]
            prey_queue.append(best_next[1])

def handler(event):
    global pause
    
    if event.char in('p'):
        pause = pause * -1
        

window.bind('<Key>', handler)

tick = 0
# For each timestep
while(1):
   
    #Build wall 
    if can_set and len(wall_horizontal.keys()+wall_vertical.keys())<max_walls:
        #build vertical wall
        if abs(x_prey-h_x) <= 4 and abs(h_x-x_prey) > 0 and prey_pos_in_box((h_x, h_y)):
           id = max(map(lambda x: int(x), wall_vertical.keys() + wall_horizontal.keys())) + 1
           wall_vertical[str(id)] = h_x
           prey_boundary = prey_update_box()
           hunter_boundary = hunter_update_box()
           (y_i, y_j) = hunter_boundary[1]
           wall_vertical_out.append((id, (h_x, y_i),( h_x, y_j)))
           canvas.create_line(h_x, y_i, h_x, y_j, fill="black")
           canvas.update()
           can_set = 0
           set_count = 0                           
           calculate_heat(predict_steps,hunter_predict_x,hunter_predict_y,h_x,h_y,heatmap)
           del prey_queue[:]
                            
        #build horizontal wall
        if abs(y_prey - h_y)<=4 and abs(y_prey - h_y) > 0 and prey_pos_in_box((h_x, h_y)):
           id = max(map(lambda x: int(x), wall_vertical.keys() + wall_horizontal.keys())) + 1
           wall_horizontal[str(id)] = h_y
           prey_boundary = prey_update_box()
           hunter_boundary = hunter_update_box()
           (x_i, x_j) = hunter_boundary[0]
           wall_horizontal_out.append((id, (x_i, h_y),( x_j, h_y))) 
           canvas.create_line(x_i, h_y, x_j, h_y, fill="black")
           canvas.update()
           can_set = 0
           set_count = 0
           calculate_heat(predict_steps,hunter_predict_x,hunter_predict_y,h_x,h_y,heatmap)
           del prey_queue[:]
             
    #Update prey   
    if tick % 2 and tick > 1:
        if not prey_queue: 
            find_safest_path(prey_queue)
            print prey_queue
        
        #There may be nothing more to do
        if prey_queue:
            prey_move = prey_queue.pop(0)
            print prey_queue
            x_prey = x_prey + prey_move[0]
            y_prey = y_prey + prey_move[1]
        
        canvas.delete('prey')
        canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
        canvas.update()
       
    #Update hunter
    if vertical_check(h_x + vx):
        vx = vx*-1
    if horizontal_check(h_y + vy):
        vy = vy*-1
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

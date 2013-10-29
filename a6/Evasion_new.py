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
x_min = -1
y_min = -1
x_max = 500
y_max = 500

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
PREY_QSIZE = 100
HUNTER_PSIZE = 2 * PREY_QSIZE
MAX_HEAT = 708

def distance(pos1,pos2):
    return math.sqrt(abs(pos1[0]-pos2[0])**2 + abs(pos1[1]-pos2[1])**2)
 
def calculate_heat(steps, pot_vx, pot_vy, pot_x, pot_y, heatmap):
    # Prediction of Hunter Moves            
    hunter_steps = []
    for i in range(HUNTER_PSIZE):
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

    # Gravity
    ((x_i, x_j), (y_i, y_j)) = prey_boundary 
    mid_x = x_i+(x_j-x_i)/2
    mid_y = y_i+(y_j-y_i)/2
    for i in range(x_prey - 100, x_prey + 100):
        for j in range(y_prey - 100, y_prey + 100):
            heatmap[i][j] = distance((i, j), (mid_x, mid_y))

    for (x, y) in hunter_steps:
        for i in range(x - 10, x + 10):
            for j in range(y - 10, y + 10):
                if distance((i, j), (x, y)) < 10 and hunter_pos_in_box((i, j)):
                    heatmap[i][j] = max(MAX_HEAT - distance((x, y), (i, j)), heatmap[i][j])

    for i in range(x_prey - 100, x_prey + 100):
        for j in range(y_prey - 100, y_prey + 100):
            img.put(str('#%02x%02x%02x' % ((255 * int(heatmap[i][j]))/MAX_HEAT, 0, 0)), (i,j))
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
        

window.bind('<Key>', handler)

tick = 0
# For each timestep
while(1):
    #Build wall 
    if can_set and len(wall_horizontal.keys()+wall_vertical.keys())<max_walls:
        #build vertical wall
        if prey_pos_in_box((h_x, h_y)) and h_x + vx == x_prey and h_x != x_prey:
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
           del prey_queue[:]
                            
        #build horizontal wall
        if prey_pos_in_box((h_x, h_y)) and h_y + vy == y_prey and h_y != y_prey:
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
           del prey_queue[:]
             
    #Update prey   
    if tick % 2 and tick > 1:
        if not prey_queue: 
            calculate_heat(predict_steps,vx,vy,h_x,h_y,heatmap)
            find_safest_path(prey_queue)
        
        #There may be nothing more to do
        if prey_queue:
            prey_move = prey_queue.pop(0)
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

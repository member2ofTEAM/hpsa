"""
Endlessly bouncing ball - demonstrates animation using Python and TKinter
"""
import time
import random
import msvcrt as m

# Initial coordinates
x0 = 0
y0 = 0

ball_diameter = 30

# Get TKinter ready to go
from Tkinter import *
import tkMessageBox
window = Tk()
canvas = Canvas(window, width=500, height=500, bg='white')
canvas.pack()

# The velocity, or distance moved per time step
vx = 1    # x velocity
vy = 1    # y velocity

# Boundaries
x_min = 0
y_min = 0
x_max = 499
y_max = 499

wall_vertical_out = [(-4,(x_min,y_min),(x_min,y_max)),(-3,(x_max,y_min),(x_max,y_max))]
wall_horizontal_out = [(-2,(x_min,y_min),(x_max,y_min)),(-1,(x_min,y_max),(x_max,y_max))]

wall_vertical = {'-4': x_min, '-3':x_max}
wall_horizontal = {'-2':y_min, '-1':y_max}

# Moves
prey_moves = {(0,1):'NN',(1,1):'NE',(1,0):'EE',(1,-1):'SE',(0,-1):'SS',(-1,-1):'SW',(-1,0):'WW',(-1,1):'NW',(0,0):'XX'}
hunter_moves = prey_moves.values() + [x+'h' for x in prey_moves.values()] + [x+'v' for x in prey_moves.values()] + ['r'+x for x in wall_horizontal.keys()+wall_vertical.keys() if int(x)>=0]

prey_queue = []
prey_move = (0,0)

x = x0
y = y0

x_prey = 330
y_prey = 200

can_set = 1

set_count = 30

pause = -1

N = 30

id = 0

max_tick = 0
best_prey = []
all_prey_moves = []

canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')

def init_values():
    global wall_vertical_out
    global wall_horizontal_out
    global wall_vertical
    global wall_horizontal
    global x
    global y
    global x_prey
    global y_prey
    global can_set
    global id
    global vx
    global vy
    global hunter_moves
    global prey_moves
    global prey_move
    global prey_queue
    global set_count
    
    # The velocity, or distance moved per time step
    vx = 1    # x velocity
    vy = 1    # y velocity
    
    # Boundaries
    x_min = 0
    y_min = 0
    x_max = 499
    y_max = 499
    
    wall_vertical_out = [(-4,(x_min,y_min),(x_min,y_max)),(-3,(x_max,y_min),(x_max,y_max))]
    wall_horizontal_out = [(-2,(x_min,y_min),(x_max,y_min)),(-1,(x_min,y_max),(x_max,y_max))]
    
    wall_vertical = {'-4': x_min, '-3':x_max}
    wall_horizontal = {'-2':y_min, '-1':y_max}
    
    # Moves
    prey_moves = {(0,1):'NN',(1,1):'NE',(1,0):'EE',(1,-1):'SE',(0,-1):'SS',(-1,-1):'SW',(-1,0):'WW',(-1,1):'NW',(0,0):'XX'}
    hunter_moves = prey_moves.values() + [x+'h' for x in prey_moves.values()] + [x+'v' for x in prey_moves.values()] + ['r'+x for x in wall_horizontal.keys()+wall_vertical.keys() if int(x)>=0]
    
    prey_queue = []
    prey_move = (0,0)
    
    x = x0
    y = y0
    
    x_prey = 330
    y_prey = 200
    
    can_set = 1
    
    set_count = 30

    id = 0
    
    pause = -1
    
    canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')

def handler(event):
    global wall_vertical_out
    global wall_horizontal_out
    global wall_vertical
    global wall_horizontal
    global x
    global y
    global x_prey
    global y_prey
    global can_set
    global id
    global vx
    global vy
    global pause

    if can_set:
                        
        
        if event.char in ('v'):
            h_walls = wall_horizontal.values()
            h_walls.sort()
            for (y_i, y_j) in zip(h_walls, h_walls[1:]):
                if y_i < y and y < y_j:
                    for i in range(10):
                        #print i
                        #print wall_vertical.keys()
                        #print wall_horizontal.keys()
                        if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                            continue
                        else:
                            id = i
                            break
                    wall_vertical[str(id)] = x
                    wall_vertical_out.append((id, (x, y_i),( x, y_j)))
                    canvas.create_line(x, y_i, x, y_j, fill="black")
                    canvas.update()
                    can_set = 0
                    set_count = 0
            #print wall_vertical

        if event.char in ('h'):
            v_walls = wall_vertical.values()
            v_walls.sort()
            for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                if x_i < x and x < x_j:
                    for i in range(10):
                        if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                            continue
                        else:
                            id = i
                            break
                    wall_horizontal[str(id)] = y
                    wall_horizontal_out.append((id, (x_i, y),( x_j, y))) 
                    canvas.create_line(x_i, y, x_j, y, fill="black")
                    canvas.update()
                    can_set = 0
                    set_count = 0
            #print wall_horizontal
            
        if event.char in ('0123456789'):
            if event.char in wall_horizontal.keys():
                wall_horizontal.pop(event.char)
                entry = [t for t in wall_horizontal_out if t[0]==int(event.char)]
                wall_horizontal_out.remove(entry[0])
                canvas.create_line(entry[0][1][0], entry[0][1][1], entry[0][2][0], entry[0][2][1], fill="white")
            elif event.char in wall_vertical.keys():
                wall_vertical.pop(event.char)
                entry = [t for t in wall_vertical_out if t[0]==int(event.char)]
                wall_vertical_out.remove(entry[0])
                canvas.create_line(entry[0][1][0], entry[0][1][1], entry[0][2][0], entry[0][2][1], fill="white")
            
            #print entry
            
            
            
         #if event.char in (wall_horizontal.keys()) or event.char in (wall_vertical.keys()):
	   

    if tick % 2:
        if event.char in ('w'):
            if not (y_prey - 1) in wall_horizontal.values():
                y_prey -= 1
            canvas.delete('prey')
            canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
            canvas.update()

        if event.char in ('a'):
            if not (x_prey - 1) in wall_vertical.values():
                x_prey -= 1
            canvas.delete('prey')
            canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
            canvas.update()

        if event.char in ('s'):
            if not (y_prey + 1) in wall_horizontal.values():
                y_prey += 1
            canvas.delete('prey')
            canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
            canvas.update()

        if event.char in ('d'):
            if not (x_prey + 1) in wall_vertical.values():
                x_prey += 1
            canvas.delete('prey')
            canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
            canvas.update()
        

    if event.char in('p') or event.char in('r'):
        pause = pause * -1
        

window.bind('<Key>', handler)

f = open("prey_moves_diag_backup", "rb")
input_text = f.read().split('\n')
#input_text = 0
#offset = input_text[-3]
rep_no = 0
prey_queue = eval(input_text[rep_no])

tick = 0
# For each timestep
while(1):
    if(pause==1):
        raw_input('World. The time has come to.. PUSH THE BUTTON')
        pause*=-1
    # Create an circle which is in an (invisible) box whose top left corner is at (x[t], y[t])
#    canvas.create_oval(x[t], y[t], x[t]+ball_diameter, y[t]+ball_diameter, fill="blue", tag='blueball')
    canvas.create_rectangle(x, y, x+4, y+4, fill="red", tag='blueball')
    
    if can_set:
    
    #build vertical wall
        if(((x_prey-x)<=6 and (x_prey-x)>=2 and prey_moves[(vx,vy)] in ('NE','EE','SE'))) or (((x-x_prey)<=6 and (x-x_prey)>=2 and prey_moves[(vx,vy)] in ('NW','WW','SW'))):
            h_walls = wall_horizontal.values()
            h_walls.sort()
            for (y_i, y_j) in zip(h_walls, h_walls[1:]):
                if y_i < y and y < y_j and y_i < y_prey and y_prey < y_j:
                    v_walls = wall_vertical.values()
                    v_walls.sort()
                    for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                        if x_i < x and x_i < x_prey and x < x_j and x_prey < x_j:
                            for i in range(len(wall_vertical.keys()+wall_horizontal.keys())):
                                if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                                    continue
                                else:
                                    id = i
                                    break
                            wall_vertical[str(id)] = x
                            wall_vertical_out.append((id, (x, y_i),( x, y_j)))
                            canvas.create_line(x, y_i, x, y_j, fill="black")
                            canvas.update()
                            can_set = 0
                            set_count = 0                           
                            
        #build horizontal wall
        if(((y_prey-y)<=6 and (y_prey-y)>=2 and prey_moves[(vx,vy)] in ('NE','NN','NW'))) or (((y_prey-y)>=-6 and (y_prey-y)<=-2 and prey_moves[(vx,vy)] in ('SE','SS','SW'))):
            h_walls = wall_horizontal.values()
            h_walls.sort()
            for (y_i, y_j) in zip(h_walls, h_walls[1:]):
                if y_i < y and y < y_j and y_i < y_prey and y_prey < y_j:
                    v_walls = wall_vertical.values()
                    v_walls.sort()
                    for (x_i, x_j) in zip(v_walls, v_walls[1:]):
                        if x_i < x and x_i < x_prey and x < x_j and x_prey < x_j:
                            for i in range(len(wall_vertical.keys()+wall_horizontal.keys())):
                                if str(i) in wall_vertical.keys()+wall_horizontal.keys():
                                    continue
                                else:
                                    id = i
                                    break
                            wall_horizontal[str(id)] = y
                            wall_horizontal_out.append((id, (x_i, y),( x_j, y))) 
                            canvas.create_line(x_i, y, x_j, y, fill="black")
                            canvas.update()
                            can_set = 0
                            set_count = 0
             
                  
    if tick % 2:
        if not input_text:
            steps = random.randint(85, 115)
    
            if len(prey_queue)==0:
                prey_queue.append(random.choice(prey_moves.keys()))
                prey_queue = prey_queue*steps     
                
            prey_move = prey_queue.pop()
            
            x_hyp = x_prey + prey_move[0]
            y_hyp = y_prey + prey_move[1]
            
            if x_hyp >= x_max or x_hyp <= x_min or x_hyp in wall_vertical.values() or y_hyp >= y_max or y_hyp <= y_min or y_hyp in wall_horizontal.values():
                prey_move = []
                for move in prey_moves.keys():
                    x_hyp = x_prey + move[0]
                    y_hyp = y_prey + move[1]
                    if x_hyp >= x_max or x_hyp <= x_min or x_hyp in wall_vertical.values() or y_hyp >= y_max or y_hyp <= y_min or y_hyp in wall_horizontal.values():
                        continue
                    else:
                        prey_move.append((move[0],move[1]))
    
                        
                prey_move = random.choice(prey_move)
                prey_queue = [prey_move]*steps 
        else:
            prey_move = prey_queue[int(tick)/2]

            
        #index = int(tick)/2
        #print index
        #prey_move = prey_queue_input[index]
        all_prey_moves.append((prey_move[0], prey_move[1]))
        x_prey = x_prey + prey_move[0]
        #x_prey = prey_move[0]
        y_prey = y_prey + prey_move[1]
        #y_prey = prey_move[1]
        canvas.delete('prey')
        canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
        canvas.update()
       

    # New coordinate equals old coordinate plus distance-per-timestep
    x = x + vx
    y = y + vy

    # If a boundary has been crossed, reverse the direction
    if x >= x_max or x <= x_min or x in wall_vertical.values():
        vx = vx*-1

    if y >= y_max or y <= y_min or y in wall_horizontal.values():
        vy = vy*-1

    

    canvas.update()

    # Pause for 0.05 seconds, then delete the image
    time.sleep(0.020)
    canvas.delete('blueball')
    tick += 1
    set_count += 1
    #print set_count
    if set_count >= N:
        can_set = 1
        
    print tick
        
    if x_prey in range(x - 4, x + 5) and y_prey in range(y - 4, y + 5):
        if max_tick < tick:
            print "Hinter wina witha " + str(tick) + " stepsaaa"
            max_tick = tick
            best_prey = all_prey_moves[:]
            #f.write(str(best_prey) + "\n")
        canvas.delete("all")
        init_values()
        tick = 0
        all_prey_moves = []
        if(rep_no < len(input_text)-1):
            rep_no += 1
            prey_queue = eval(input_text[rep_no])
        else:
            quit()

f.close()

# I don't know what this does but the script won't run without it.
window.mainloop()

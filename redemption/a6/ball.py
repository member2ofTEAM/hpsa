"""
Endlessly bouncing ball - demonstrates animation using Python and TKinter
"""
import time

# Initial coordinates
x0 = 0
y0 = 0

ball_diameter = 30

# Get TKinter ready to go
from Tkinter import *
window = Tk()
canvas = Canvas(window, width=500, height=500, bg='white')
canvas.pack()

# The velocity, or distance moved per time step
vx = 1    # x velocity
vy = 1    # y velocity

# Boundaries
x_min = 0
y_min = 0
x_max = 500
y_max = 500

# Moves
prey_moves = ['NN','NE','EE','SE','SS','SW','WW','NW']
hunter_moves = prey_moves + [x+'h' for x in prey_moves] + [x+'v' for x in_prey_moves] + ['r'+x for x in wall_horizontal_our.keys()+wall_vertical_our.keys() if int(x)>=0]

 
wall_vertical = [(-4,(x_min,y_min),(x_min,y_max)),(-3,(x_may,y_min),(x_max,y_may))]
wall_horizontal = [(-2,(x_min,y_min),(x_max,y_min)),(-1,(x_min,y_max),(x_m

wall_vertical_our = {'-4': x_min, '-3':x_max}
wall_horizontal:our = {'-2':y_min, '-1':y_max}

x = x0
y = y0

x_prey = 330
y_prey = 200

can_set = 1

N = 10

canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')

def handler(event):
    global wall_vertical
    global wall_horizontal
    global x
    global y
    global x_prey
    global y_prey
    global can_set

    if can_set:
        if event.char in ('v'):
            wall_vertical_our[v_id] = x
            wall_vertical.sort()
            for (y_i, y_j) in zip(wall_horizontal, wall_horizontal[1:]):
                if y_i < y and y < y_j:
		    wall_vertical.append(v_id, (x, y_i),( x, y_j)) 
		    v_id = v_id + 1
                    canvas.create_line(x, y_i, x, y_j, fill="black")
                    canvas.update()
                    can_set = 0
            print wall_vertical

        if event.char in ('h'):
            wall_horizontal_our[h_id] = y
            wall_horizontal.sort()
            for (x_i, x_j) in zip(wall_vertical, wall_vertical[1:]):
                if x_i < x and x < x_j:
		     wall_horizontal.append(h_id, (x, y_i),( x, y_j)) 
		     h_id = h_id + 1
                    canvas.create_line(x_i, y, x_j, y, fill="black")
                    canvas.update()
                    can_set = 0
            print wall_horizontal
            
         if event.char in (wall_horizontal.keys()) or event.char in (wall_vertical.keys()):
	   

    if tick % 2:
        if event.char in ('w'):
            if not (y_prey - 1) in wall_horizontal:
                y_prey -= 1
            canvas.delete('prey')
            canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
            canvas.update()

        if event.char in ('a'):
            if not (x_prey - 1) in wall_vertical:
                x_prey -= 1
            canvas.delete('prey')
            canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
            canvas.update()

        if event.char in ('s'):
            if not (y_prey + 1) in wall_horizontal:
                y_prey += 1
            canvas.delete('prey')
            canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
            canvas.update()

        if event.char in ('d'):
            if not (x_prey + 1) in wall_vertical:
                x_prey += 1
            canvas.delete('prey')
            canvas.create_rectangle(x_prey, y_prey, x_prey + 4, y_prey + 4, fill = "blue", tag = 'prey')
            canvas.update()

window.bind('<Key>', handler)

tick = 0
# For each timestep
while(1):
    # Create an circle which is in an (invisible) box whose top left corner is at (x[t], y[t])
#    canvas.create_oval(x[t], y[t], x[t]+ball_diameter, y[t]+ball_diameter, fill="blue", tag='blueball')
    canvas.create_rectangle(x, y, x+4, y+4, fill="red", tag='blueball')

    # New coordinate equals old coordinate plus distance-per-timestep
    x = x + vx
    y = y + vy

    # If a boundary has been crossed, reverse the direction
    if x >= x_max or x <= x_min or x in wall_vertical:
        vx = vx*-1

    if y >= y_max or y <= y_min or y in wall_horizontal:
        vy = vy*-1

    if x_prey in range(x - 4, x + 5) and y_prey in range(y - 4, y + 5):
        print "Hinter wina witha " + str(tick) + " stepsaaa"
        break

    canvas.update()

    # Pause for 0.05 seconds, then delete the image
    time.sleep(0.005)
    canvas.delete('blueball')
    tick += 1
    if tick % N:
        can_set = 1

# I don't know what this does but the script won't run without it.
window.mainloop()

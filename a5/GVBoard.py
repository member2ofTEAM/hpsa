'''
Created on 13.10.2013

@author: Sven
'''
from Tkinter import *
import random
from PIL import Image
import colorsys
import math

#CANVAS_Size
canvas_width = 1000
canvas_height = 1000

#COLORS
player1_area = (0,0,1) # blue
player2_area = (1,0,0) # red

player1 = (0,0,1)
player2 = (1,0,0)

border = (0,0,0) #black 
background = (255,255,255) #white

#BOARD
board = []
maxval = 1
minval = 0

#GAMESTATES
game_states = []

def read_game_states():
    f = open('a', 'r')
    i = 0
    j = 0
    state = []
    while(True):
        if(((i%1000)==0) and (i!=0)):
            game_states.append(state)
            state = []
            read_board(j)
            create_image()
            display_image()
            j = j+1
            
        a = f.readline()
        b = a.split()
        if(len(a)>0):
            state.append(b)
            i = i+1
            print i
        else:
            break


  
def read_board(state):
    f = game_states[state]
    maxval = 1
    minval = 0
    for line in f:
        row = []
        for value in line:
            row.append(float(value))
            if(abs(float(value)))>maxval:
	      maxval = abs(float(value))
            if(abs(float(value)))<minval:
	      minval = abs(float(value))
        #Go down one row
        board.append(row)   
    
'''    
def read_board():
    f = open('b.txt', 'r')
    maxval = 1
    for line in f:
        row = []
        split = line.split()
        for value in split:
            row.append(float(value))
            if(float(value))>maxval:
                maxval = float(value)
        #Go down one row
        board.append(row)   
'''
        
def create_image(): 
    img = Image.new( 'RGB', (1000,1000), "black") # create a new black image
    pixels = img.load() # create the pixel map
     
    for i in range(img.size[0]):    # for every pixel:
        for j in range(img.size[1]):
            if(board[i][j]==10000000):
                print "player1"
		pixels[i,j] = (player1[0]*255,player1[1]*255,player1[2]*255)
            elif(board[i][j]==-10000000):
                print "player2"
                pixels[i,j] = (player2[0]*255,player2[1]*255,player2[2]*255)
            elif(board[i][j]>0):
                p_color = colorsys.rgb_to_hsv(player1_area[0], player1_area[1], player1_area[2])
                value = [p_color[0],p_color[1],p_color[2]]
                value[1] = math.sqrt(math.sqrt(math.sqrt(abs(board[i][j]))))
                value = colorsys.hsv_to_rgb(value[0], value[1], value[2])
                pixels[i,j] = (int(value[0]*255),int(value[1]*255),int(value[2]*255)) # set the colour accordingly
            elif(board[i][j]<0):
                p_color = colorsys.rgb_to_hsv(player2_area[0], player2_area[1], player2_area[2])
                value = [p_color[0],p_color[1],p_color[2]]
                value[1] = math.sqrt(math.sqrt(math.sqrt(abs(board[i][j]))))
                value = colorsys.hsv_to_rgb(value[0], value[1], value[2])
                pixels[i,j] = (int(value[0]*255),int(value[1]*255),int(value[2]*255)) # set the colour accordingly
            else:
                pixels[i,j] = background
     
    
    img.save('board.gif')
        
def display_image():    
    master = Tk()
    
    w = Canvas(master, 
               width=canvas_width, 
               height=canvas_height)
    w.pack()
    
    w.create_rectangle(0, 0, canvas_width-1, canvas_height-1, fill='white')
    
    
    img = PhotoImage(file="board.gif")
    w.create_image(20,20, anchor=NW, image=img)
    mainloop()
    
read_game_states()
'''
for i in range(len(game_states)):
    read_board(i)
    create_image()
    display_image()
'''

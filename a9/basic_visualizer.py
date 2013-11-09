from Tkinter import *
import argparse
import random
from sets import Set
import operator
import socket

#The Player Class
class Player():
  def __init__(self,teamid,teamname,money,time):
    self.teamid = teamid
    self.teamname = teamname
    self.money = money
    self.time = time
    
    self.current_bid = 0
    
    self.items = {}
    
  def update(time_used, bid,item_won=-1):
    if item_won!=-1:
      self.money = max(self.money - self.current_bid,0)
      if item_won in self.items:
	self.items[item_won] = self.items.get(item_won) + 1
      else:
	self.items[item_won] = 1
	
    self.time = max(self.time - time_used, 0)
    self.current_bid = bid

players = [] #list containing the player-objects



pot_item_names = ['Balisto','Daim', 'Excellence', 'Flake', 'Godiva', 
		   'Hay Hay', 'Idaho Spud', 'KitKat','Lion', 'Mars',
		   'Noisette', 'Oreo', 'Penguin', 'Rolo', 'Snickers',
		   'Twix', 'UnoBar', 'Valomilk', 'WunderBar','Yorkie',
		   'Zero Bar'] 
		   
random.shuffle(pot_item_names)

item_names = ['Almond Joy','Caramello Koala']
item_colors= ['red','blue','magenta','purple','white','darkblue','brown',
	      'violet','darkgreen','orange']
random.shuffle(item_colors)




#Create argument-variables and Parse arguments
parser = argparse.ArgumentParser(description='Process input.')
parser.add_argument('goal', metavar='g',
		    help='Number of items of the same type needed to win')
parser.add_argument('team_list', metavar='t', nargs='+',
		    help='name1 time1 name2 time2 ... - in case parakeet is used')
parser.add_argument('init_money', metavar='m', type=int,
                   help='Money per player')
parser.add_argument('itemlist', metavar='i',
		    help='List with items in order of occurence')
parser.add_argument('port', metavar='pn', type=int,
		    help='The port number - for server communication')
		    
		    
args = parser.parse_args()


#Create all Player instances
for i in range(0,len(args.team_list),2):
  teamid = i/2
  name = args.team_list[i]
  money = args.init_money
  time = int(args.team_list[i+1])
  
  new_player = Player(teamid,name,money,time)
  players.append(new_player)
  
  

  
#Create item names
diff_items = len(Set(args.itemlist))
for i in range(int(diff_items)-2):
  item_names.append(pot_item_names.pop())
  
item_names.sort()

print item_names


#Open itemlist specified from arguments
#And read in file
input = open(args.itemlist)
item_list = input.read()
input.close()

#Create list of items as integers
item_list = item_list.split(" ")
i_list = []

for item in item_list:
  i_list.append(int(item))

#Current item
current_item = i_list.pop()
last_item = 0
last_winner = 1





master = Tk()

#Height is dependent on number of players
w = Canvas(master, width=550, height=70*len(players)+10*len(players)+140)
w.pack()


def draw_scoreboard():
  x_offset=10
  y_offset=10
    
  #draw status
  text_in='Current item:'
  w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
  x_offset += len(text_in)*6+20
  item = item_names[current_item]
  w.create_oval((x_offset,y_offset+1,x_offset+12,y_offset+3+10),fill=item_colors[current_item])
  w.create_text((x_offset+2,y_offset),text=item[0],justify='left',anchor='nw')
  x_offset+=15
  w.create_text((x_offset,y_offset),text=item,justify='left',anchor='nw',fill=item_colors[current_item])
  x_offset+=len(item)*6+20  
  text_in='Last item:'
  w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
  x_offset += len(text_in)*6+5
  item = item_names[last_item]
  w.create_oval((x_offset,y_offset+1,x_offset+12,y_offset+3+10),fill=item_colors[last_item])
  w.create_text((x_offset+2,y_offset),text=item[0],justify='left',anchor='nw')
  x_offset+=15
  w.create_text((x_offset,y_offset),text=item,justify='left',anchor='nw',fill=item_colors[last_item])
  x_offset+=len(item)*6+20  
  text_in='Last Winner:'
  w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
  x_offset+=len(item)*6+20 
  w.create_text((x_offset,y_offset),text=players[last_winner].teamname,justify='left',anchor='nw')
  x_offset=10
  y_offset+=30
  text_in='Next '+str(min(int(args.goal),len(i_list)))+' items:'
  w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
  x_offset+=len(text_in)*6+20
  for i in range(min(int(args.goal), len(i_list))):
    item = item_names[i_list[i]]
    w.create_oval((x_offset,y_offset+1,x_offset+12,y_offset+10+3),fill=item_colors[i_list[i]])
    w.create_text((x_offset+2,y_offset),text=item[0],justify='left',anchor='nw')
    x_offset+=15
    w.create_text((x_offset,y_offset),text=item,justify='left',anchor='nw',fill=item_colors[i_list[i]])
    x_offset+=len(item)*6+20  

  y_offset+=27

  w.create_line(0, y_offset, 600, y_offset)

  y_offset+=27

  for player in players:
    x_offset=30
    text_in=player.teamname+":"
    w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw',fill='red')
    x_offset=100
    text_in='Items:'
    w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
    x_offset+=len(text_in)*6+20
    for (key,value) in sorted(player.items.iteritems(), key=operator.itemgetter(1),reverse=True):
      text_in=str(value)+"* "
      w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
      x_offset+=len(text_in)*6
      item = item_names[key]
      w.create_oval((x_offset,y_offset+2,x_offset+10,y_offset+12),fill=item_colors[key])
      w.create_text((x_offset+1,y_offset),text=item[0],justify='left',anchor='nw')
      x_offset+=15
      w.create_text((x_offset,y_offset),text=item,justify='left',anchor='nw')
      x_offset+=len(item)*6+20  
    x_offset=100
    y_offset+=35
    text_in='Current Bid:'
    w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
    x_offset+=len(text_in)*6+20
    text_in=str(player.current_bid)
    w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
    x_offset+=len(text_in)*6+20
    text_in='Money left:'
    w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
    x_offset+=len(text_in)*6+20
    text_in=str(player.money)
    w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
    x_offset+=len(text_in)*6+20
    text_in='Time left:'
    w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
    x_offset+=len(text_in)*6+20
    text_in=str(player.time)
    w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')
    y_offset+=45
    
  w.create_line(0, y_offset, 600, y_offset)
  x_offset=10
  y_offset+=30
  #draw head
  x_offset+=400
  text_in='Goal: '+args.goal+' similar items'
  w.create_text((x_offset,y_offset),text=text_in,justify='left',anchor='nw')


draw_scoreboard()

'''
#TODO: COMMUNICATION WITH SERVER - MAIN SCRIPT IS HERE
game = True
#Communication with Server:
while(game):
  messages = len(players)
  received = 0
  
  while received < messages:
    #Receive player_id bid time_used 
    draw_scoreboard()
    
  #pid = receive player_id
  for i in range(len(players)):
    if i == pid:
      players[i].update(0,0,current_item)
      last_winner = players[i].teamname
      last_item = current_item
      current_item = i_list.pop()
    else:
      players[i].update(0,0)
  
  draw_scoreboard()
''' 
mainloop()
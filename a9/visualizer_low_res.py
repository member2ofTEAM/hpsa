from Tkinter import *
import random
from sets import Set
import operator
import time

strategies =  ['Greed','No Bidding','Item Pickup','NanoBidding','Bidvasion','Bidding Salesman','Gravity Bidding','Bidforce','RandomBid','Simulated Bidding','K-Bids']
random.shuffle(strategies)

class Visualizer():
    
    class Player():
        def __init__(self, teamid, teamname, money, time, strategy = "", image=''):
            self.teamid = teamid
            self.teamname = teamname
            self.money = money
            self.time = time/1000
            self.strategy = strategy
            if self.strategy=="":
                random.shuffle(strategies)
                self.strategy = strategies.pop(0)
        
            self.image = image
            self.current_bid = 0
            self.time_used = 0
        
            self.items = {}
    
        def update(self, bid, time_used, item_won=-1):
            if item_won != -1:
                self.money = max(self.money - self.current_bid, 0)
                if item_won in self.items:
                    self.items[item_won] = self.items.get(item_won) + 1
                else:
                    self.items[item_won] = 1
        
            self.time = max(self.time - time_used, 0)
            self.current_bid = bid
            self.current_time = time_used
     
    # The Player Class
    
    
    def make_dark(self, image):
        dark = image.copy()
        for x in range(dark.width()):
            for y in range(dark.height()):
                a = dark.get(x,y)
                if (a[0] != '0') or (a[2] != '0') and (a[4] != '0'):
                    dark.put("black",(x,y))
        

        return dark
        
    def shasha_says(self,text,pause=0, delete=True):
        if pause == 0:
            pause = 0.5 + len(text)/25. 
        self.w.create_image(((self.width*3/4)+110,(self.height/6)+40),image=self.bubble,anchor='se', tag="bubble")
        shasha = text
        self.w.create_text(((self.width*3/4),(self.height/6)-30), font=("Arial",11), text = shasha, justify="center", anchor = 'center', tag = "shasha")
        self.w.update()
        time.sleep(pause)
        if delete:
            self.w.delete("shasha")
            self.w.delete("bubble")
            
        
    def screen_says(self,text,pause = 3, font=("Arial",30), pos=(300,150)):
        shasha = text
        self.w.create_text(pos, text = shasha, anchor = 'center', font=font, justify='center', tag = "screen")
        self.w.update()
        time.sleep(pause)
    
    def intro(self):
        self.set_podiums(-2,-1, True)
        self.draw_scoreboard(-1,-1, True)
        
        self.shasha_says("Welcome to tonight's game.")
        self.shasha_says("This will be a lot of fun!")
        self.shasha_says("I guess everyone of us has\n participated in an auction")
        self.shasha_says("since the rise of webbased\n auction sites like eBay.")
        self.shasha_says("But the game we play tonight\n is not a regular auction.")
        self.shasha_says("It is...")
        self.screen_says("CAUTION\nThe Candy Auction", 0)
        self.shasha_says("... Caution!\nThe Candy Auction.",5)
        self.shasha_says("Every round I will offer you a\nparticular candy.")
        self.shasha_says("There will be\n " + str(self.diff_items)+ " different types of candy.")
        self.shasha_says("The first team that manages to\n win "+str(self.goal)+" candies of the same type")
        self.shasha_says("will win the auction and\n receive something special!")
        self.shasha_says("It's kind of a metaphor for\n this course, isn't it?")
        self.shasha_says("Tonight we have\n "+str(len(self.players)) + " competitors.")
        
        for i in range(len(self.players)):
            self.shasha_says("Our "+str(i+1)+". team is")
            self.w.delete("screen")
            self.set_podiums(-2, i, True)
            self.screen_says(self.players[i].teamname,0)
            self.shasha_says(self.players[i].teamname,3)
            self.shasha_says("Please come on stage and\n present us your strategy:")
            self.screen_says(self.players[i].strategy, 0,pos=(300,200))
            self.shasha_says(self.players[i].strategy)
            raw_input()
                  
    def __init__(self, goal, team_list, itemlist, init_money=100, intro = 1):
        self.goal = goal
        self.players = []
        self.pot_item_names = ['Balisto', 'Daim', 'Excellence', 'Flake', 'Godiva',
                               'Hay Hay', 'Idaho Spud', 'KitKat', 'Lion', 'Mars',
                               'Noisette', 'Oreo', 'Penguin', 'Rolo', 'Snickers',
                               'Twix', 'UnoBar', 'Valomilk', 'WunderBar', 'Yorkie',
                               'Zero Bar']
        
        self.pot_item_names = ['Godiva','Mars','Snickers','Twix', 'Oreo', 'Milky Way', 'Reeses','Zero']        
        self.item_names = ['Almond Joy', 'Caramello']
        
        
        self.item_colors = ['red', 'blue', 'magenta', 'purple', 'grey', 'darkblue', 'brown',
                            'violet', 'darkgreen', 'orange']
        
        random.shuffle(self.item_colors)
        
        self.itemlist = itemlist[:]
        random.shuffle(self.pot_item_names)
            # Create all Player instances
        for i in range(0, len(team_list)):
            teamid = i
            name = team_list[i][0]
            money = init_money
            time = int(team_list[i][1])
            strategy = team_list[i][2]
            image = team_list[i][3]
            
            new_player = self.Player(teamid, name, money, time,strategy,image)
            self.players.append(new_player)
          
        # Create item names
        self.diff_items = len(Set(itemlist))
        for i in range(int(self.diff_items) - 2):  # -2 because almond and caramel are always in
            self.item_names.append(self.pot_item_names.pop())
          
        self.item_names.sort()
        
        self.item_files = [x.replace(' ','_') for x in self.item_names]
        print self.item_files
    
        print self.item_names
        
        
        # Current item
        self.current_bid = 0
        self.current_time = 0
        self.current_high = ''
        self.current_item = self.itemlist.pop(0)
        self.last_item = -1
        self.last_winner = -1
        
        self.bidqueue = []

        self.master = Tk()
        
        self.labelList = []
        
        self.tkimage = []
        self.darkimage = []
        self.randomimage = []
        
        self.candyimage = []
        self.small_candy = []
        
        self.kitkat = (PhotoImage(file="Images_low/Kit_Kat.gif"))
        
        for i in range(self.diff_items):
            self.candyimage.append(PhotoImage(file="Images_low/"+self.item_files[i]+".gif"))
            self.small_candy.append(PhotoImage(file="Images_low/"+self.item_files[i]+"_small.gif"))
        
        
        for i in range(11):
            str_num = str(i+1)
            self.randomimage.append(PhotoImage(file="Images_low/picture"+str_num+".gif"))
        for i in range(len(self.players)):
            if(self.players[i].image == ""):
                random.shuffle(self.randomimage)
                self.tkimage.append(self.randomimage.pop(0))
            else:
                self.tkimage.append(PhotoImage(file="Images_low/"+self.players[i].image))
            #self.darkimage.append(self.make_dark(self.tkimage[i]))
            self.darkimage.append(self.make_dark(self.tkimage[i]))
                     
        #random.shuffle(self.tkimage)
        
        self.numimage = []
        for i in range(10):
            str_num = str(i)
            self.numimage.append(PhotoImage(file="Images_low/"+str_num+".gif"))
        
        self.numimage.append(PhotoImage(file="Images_low/number_template.gif"))
        self.numimage.append(PhotoImage(file="Images_low/W.gif"))
        self.numimage.append(PhotoImage(file="Images_low/I.gif"))
        self.numimage.append(PhotoImage(file="Images_low/N.gif"))
        self.numimage.append(PhotoImage(file="Images_low/x_1.gif"))
        self.podium = PhotoImage(file="Images_low/podium2.gif")
        self.shasha= PhotoImage(file="Images_low/shasha.gif")
        self.bubble= PhotoImage(file="Images_low/bubble.gif")
        
        # Height is dependent on number of players
        self.width = 1000
        self.height = 700 
        
        self.w = Canvas(self.master, width=self.width, height=self.height)
        self.w.pack()
        
        if intro:
            self.intro()
        
        self.draw_scoreboard(-1)
        
        
    def set_podiums(self, state, pid=-1, intro = False):
    
        no_players = len(self.players)
        width = self.width
        height = self.height
        
        if(no_players<=4):
            player_box_upper_y = height/3
            player_box_y_offset = height - player_box_upper_y
            player_box_left_x = 0
            player_box_x_offset = width/no_players
            
            for player in self.players:
                self.labelList.append(self.tkimage[player.teamid])
                center_x = player_box_left_x + (player_box_x_offset/2)
                center_y = player_box_upper_y + (player_box_y_offset/2)
                if intro and player.teamid > pid:
                    self.w.create_image((center_x,center_y-60),image=self.darkimage[player.teamid],anchor='s')
                    self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                    self.w.create_text((center_x,center_y-53),text="???",font=("Arial",8),anchor='center')
                    self.w.create_text((center_x,center_y-38),text="???",font=("Arial",8),anchor='center')
                else:
                    self.w.create_image((center_x,center_y-60),image=self.tkimage[player.teamid],anchor='s')
                    self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                    self.w.create_text((center_x,center_y-53),text=player.teamname,font=("Arial",8),anchor='center')
                    self.w.create_text((center_x,center_y-38),text=player.strategy,font=("Arial",8),anchor='center')
                #self.w.create_rectangle(center_x-75,center_y-100,center_x+75,center_y+100,fill="brown")
                player_box_left_x += player_box_x_offset

                if(state==-1):
                    if((player.teamid == pid) or ((player.teamid in self.bidqueue) and (self.bidqueue.index(player.teamid)<self.bidqueue.index(pid)))):
                        if player.current_bid < 10:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                        elif player.current_bid < 100:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[2])],anchor='center')
                    else:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[-1],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",12), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                    #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    #self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                elif state == 0:
                    if player.teamid in self.bidqueue:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[-1],anchor='center')
                    else:        
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[10],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                    #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    
                        
                else:
                    if player.teamid == pid and not intro:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[11],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[12],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[13],anchor='center')
                    else:
                        if player.money < 10:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                        elif player.money < 100:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.money)[1])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[2])],anchor='center')
                    for (key, value) in sorted(player.items.iteritems(), key=operator.itemgetter(1), reverse=True)[:1]:
                        text_in = str(value) + "* "
                        self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",15), justify='left', anchor='nw')
                        item = self.item_names[key]
                        
                        self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                        #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                        #self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                
                self.w.create_text((center_x,center_y+50),text="Time left:  " + str(int(player.time)),font=("Arial",10),anchor='center')
                       
        if(no_players>4):  
            if(no_players%2):
                upper = (no_players/2)+1 
            else:
                upper = no_players/2
            i=0    
    
    
            player_box_upper_y = height/3
            player_box_y_offset = height - player_box_upper_y
            player_box_left_x = 0
            player_box_x_offset = width/upper
            
            while i<upper:
                player = self.players[i]
                center_x = player_box_left_x + (player_box_x_offset/2)
                center_y = player_box_upper_y + (player_box_y_offset/2) - 25
                if intro and player.teamid > pid:
                    self.w.create_image((center_x,center_y-60),image=self.darkimage[player.teamid],anchor='s')
                    self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                    self.w.create_text((center_x,center_y-53),text="???",font=("Arial",8),anchor='center')
                    self.w.create_text((center_x,center_y-38),text="???",font=("Arial",8),anchor='center')
                else:
                    self.w.create_image((center_x,center_y-60),image=self.tkimage[player.teamid],anchor='s')
                    self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                    self.w.create_text((center_x,center_y-53),text=player.teamname,font=("Arial",8),anchor='center')
                    self.w.create_text((center_x,center_y-38),text=player.strategy,font=("Arial",8),anchor='center')
                #self.w.create_rectangle(center_x-75,center_y-100,center_x+75,center_y+100,fill="brown")
                player_box_left_x += player_box_x_offset

                if(state==-1):
                    if((player.teamid == pid) or ((player.teamid in self.bidqueue) and (self.bidqueue.index(player.teamid)<self.bidqueue.index(pid)))):
                        if player.current_bid < 10:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                        elif player.current_bid < 100:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[2])],anchor='center')
                    else:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[-1],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",12), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                    #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    #self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                elif state == 0:
                    if player.teamid in self.bidqueue:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[-1],anchor='center')
                    else:        
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[10],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                    #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    
                        
                else:
                    if player.teamid == pid and not intro:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[11],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[12],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[13],anchor='center')
                    else:
                        if player.money < 10:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                        elif player.money < 100:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.money)[1])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[2])],anchor='center')
                    for (key, value) in sorted(player.items.iteritems(), key=operator.itemgetter(1), reverse=True)[:1]:
                        text_in = str(value) + "* "
                        self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",15), justify='left', anchor='nw')
                        item = self.item_names[key]
                        
                        self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                        #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                        #self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                
                self.w.create_text((center_x,center_y+50),text="Time left:  " + str(int(player.time)),font=("Arial",10),anchor='center')
                       
                i+=1
    
            player_box_upper_y = height/3
            player_box_y_offset = height - player_box_upper_y
            player_box_left_x = 0
            player_box_x_offset = width/(no_players-upper)
            
            while(i<no_players):
                player = self.players[i]
                center_x = player_box_left_x + (player_box_x_offset/2)
                center_y = player_box_upper_y + (player_box_y_offset/2) + (player_box_y_offset/2)/2 + 45
                if intro and player.teamid > pid:
                    self.w.create_image((center_x,center_y-65),image=self.darkimage[player.teamid],anchor='s')
                    self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                    self.w.create_text((center_x,center_y-53),text="???",font=("Arial",8),anchor='center')
                    self.w.create_text((center_x,center_y-38),text="???",font=("Arial",8),anchor='center')
                else:
                    self.w.create_image((center_x,center_y-65),image=self.tkimage[player.teamid],anchor='s')
                    self.w.create_image((center_x,center_y-10),image=self.podium,anchor='center')
                    self.w.create_text((center_x,center_y-53),text=player.teamname,font=("Arial",8),anchor='center')
                    self.w.create_text((center_x,center_y-38),text=player.strategy,font=("Arial",8),anchor='center')
                #self.w.create_rectangle(center_x-75,center_y-100,center_x+75,center_y+100,fill="brown")
                player_box_left_x += player_box_x_offset

                if(state==-1):
                    if((player.teamid == pid) or ((player.teamid in self.bidqueue) and (self.bidqueue.index(player.teamid)<self.bidqueue.index(pid)))):
                        if player.current_bid < 10:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                        elif player.current_bid < 100:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[int(str(player.current_bid)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.current_bid)[1])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.current_bid)[2])],anchor='center')
                    else:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[-1],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",12), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                    #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    #self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                        
                elif state == 0:
                    if player.teamid in self.bidqueue:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[-1],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[-1],anchor='center')
                    else:        
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[10],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[10],anchor='center')
                    if self.current_item in player.items:
                        (key,value) = (self.current_item,player.items[self.current_item])
                    else:
                        (key,value) = (self.current_item,0)
                    text_in = str(value) + "* "
                    self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",15), justify='left', anchor='nw')
                    item = self.item_names[key]
                    self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                    #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                    
                        
                else:
                    if player.teamid == pid and not intro:
                        self.w.create_image((center_x-27,center_y-8),image=self.numimage[11],anchor='center')
                        self.w.create_image((center_x,center_y-8),image=self.numimage[12],anchor='center')
                        self.w.create_image((center_x+27,center_y-8),image=self.numimage[13],anchor='center')
                    else:
                        if player.money < 10:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                        elif player.money < 100:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[0],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[1])],anchor='center')
                        else:
                            self.w.create_image((center_x-27,center_y-8),image=self.numimage[int(str(player.money)[0])],anchor='center')
                            self.w.create_image((center_x,center_y-8),image=self.numimage[int(str(player.money)[1])],anchor='center')
                            self.w.create_image((center_x+27,center_y-8),image=self.numimage[int(str(player.money)[2])],anchor='center')
                    for (key, value) in sorted(player.items.iteritems(), key=operator.itemgetter(1), reverse=True)[:1]:
                        text_in = str(value) + "* "
                        self.w.create_text((center_x-25, center_y+20), text=text_in, font=("Arial",15), justify='left', anchor='nw')
                        item = self.item_names[key]
                        
                        self.w.create_image((center_x+5,center_y+26), image=self.small_candy[key], anchor="center")
                        #self.w.create_oval((center_x-16, center_y +26, center_x + 16, center_y+36 + 20 + 3), fill=self.item_colors[key])
                        #self.w.create_text((center_x + 1, center_y+40), text=item[0], justify='left', anchor='center')
                
                self.w.create_text((center_x,center_y+50),text="Time left:  " + str(int(player.time)),font=("Arial",10),anchor='center')
                       
                i+=1
      
        
    def draw_scoreboard(self,end, pid=-1, intro = False):
        self.w.create_line(5, 5, 600, 5)

        x_offset = 10
        y_offset = 10
        
        
        self.w.create_image(((self.width*3/4)+150,(self.height/6)+100),image=self.shasha,anchor='center')
        
        if(intro):
            pass    
        elif(end==-1):
            # draw status
            text_in = 'Last item:'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            x_offset += len(text_in) * 6 + 5
            if(self.last_item > -1):
                item = self.item_names[self.last_item]
                self.w.create_oval((x_offset, y_offset + 1, x_offset + 12, y_offset + 3 + 10), fill=self.item_colors[self.last_item])
                self.w.create_text((x_offset + 2, y_offset), text=item[0], justify='left', anchor='nw')
                x_offset += 15
                self.w.create_text((x_offset, y_offset), text=item, justify='left', anchor='nw', fill=self.item_colors[self.last_item])
                x_offset += len(item) * 6 + 20  
            text_in = 'Last Winner:'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            x_offset += len(text_in) * 6 + 10
            if(self.last_winner > -1):
                self.w.create_text((x_offset, y_offset), text=self.last_winner, justify='left', anchor='nw')
            x_offset = 10
            y_offset += 30
            text_in = 'Next ' + str(min(int(self.goal), len(self.itemlist), 5)) + ' items:'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            x_offset += len(text_in) * 6 + 20
            for i in range(min(int(self.goal), len(self.itemlist))):
                item = self.item_names[self.itemlist[i]]
                self.w.create_oval((x_offset, y_offset + 1, x_offset + 12, y_offset + 10 + 3), fill=self.item_colors[self.itemlist[i]])
                self.w.create_text((x_offset + 2, y_offset), text=item[0], justify='left', anchor='nw')
                x_offset += 15
                self.w.create_text((x_offset, y_offset), text=item, justify='left', anchor='nw', fill=self.item_colors[self.itemlist[i]])
                x_offset += len(item) * 6 + 20  

            y_offset += 27
            
            self.w.create_line(10, y_offset, 600, y_offset)
            
            y_offset += 10
            
            x_offset = 20
            text_in = 'Current item:'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            x_offset += len(text_in) * 6 + 20
            item = self.item_names[self.current_item]
            self.w.create_image((x_offset+180,y_offset+75), image=self.candyimage[self.current_item], anchor="center")
            x_offset += 180
            self.w.create_text((x_offset, y_offset+150), text=item, justify='center', font=("Arial",30), anchor='center', fill=self.item_colors[self.current_item]) 
            y_offset += 210
            self.w.create_text((20, y_offset), text="Current best bid: "+str(self.current_bid) +"        Time needed: "+str(self.current_time)+"         by "+self.current_high, justify='left', anchor='nw')
        elif end == -2:
            ranking = self.players[:]
            ranking.sort(key = lambda x: max(x.items.values(),0),reverse=True)
            for player in ranking:
                x_offset = 30
                text_in = player.teamname + ":"

                self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw', fill='red')
                x_offset = 175
                text_in = 'Items:'
                self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
                x_offset += len(text_in) * 6 + 20
                for (key, value) in sorted(player.items.iteritems(), key=operator.itemgetter(1), reverse=True)[:4]:
                    text_in = str(value) + "* "
                    self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
                    x_offset += len(text_in) * 6
                    item = self.item_names[key]
                    self.w.create_oval((x_offset, y_offset + 1, x_offset + 12, y_offset + 10 + 3), fill=self.item_colors[key])
                    self.w.create_text((x_offset + 1, y_offset), text=item[0], justify='left', anchor='nw')
                    x_offset += 15
                    self.w.create_text((x_offset, y_offset), text=item, justify='left', anchor='nw')
                    x_offset += len(item) * 6 + 20  
                x_offset = 100
                y_offset += 25
            
            self.w.create_line(10, y_offset, 600, y_offset)
            x_offset = 10
            y_offset += 5
            # draself.w.head
            x_offset += 400
            text_in = 'Goal: ' + str(self.goal) + ' similar items'
            self.w.create_text((x_offset, y_offset), text=text_in, justify='left', anchor='nw')
            y_offset += 20
            
        else:
            self.w.create_text((300,70),text="CONGRATULATIONS\n\n"+self.players[pid].teamname,font=('Arial',30),anchor="center",justify="center")
            self.w.create_image((300,200), image=self.kitkat, anchor="center")
            self.w.create_text((300, 290), text="KIT KAT", justify='center', font=("Arial",30), anchor='center', fill='red') 
 
        
        final_y = self.height/3 + (self.height - self.height/3)/4 - 40
        
        self.w.create_line(5, 5, 5, final_y)
        self.w.create_line(600, 5, 600, final_y)
        self.w.create_line(5, final_y, 600, final_y)
        self.w.update()
        
        
    #TODO: COMMUNICATION WITH SERVER - MAIN SCRIPT IS HERE
    #TODO: DISPLAY WINNER OF THE GAME
    #Overloaded function:
    #for every given bid: id,bid,time_used (for every team)
    #if item is won: id,-1 (only once for the winner)
    #if game is won: id only for the winner
    def update(self, pid, bid=-2, time_used=0):
        time_used = time_used/1000
        print time_used
        if bid >=0:
            self.bidqueue.append(pid)
            self.players[pid].update(bid,time_used)
            self.w.delete("all")
            self.set_podiums(0,pid)
            self.draw_scoreboard(-1,pid)
            self.w.update()
        elif bid==-1:
            for i in self.bidqueue:
                self.w.delete("all")
                if(self.players[i].current_bid > self.current_bid):
                    self.current_bid = self.players[i].current_bid
                    self.current_time = self.players[i].time_used
                    self.current_high = self.players[i].teamname
                self.set_podiums(-1,i)
                self.draw_scoreboard(-1,i)
                self.w.update()
                time.sleep(2)
            self.current_bid = 0
            self.current_time = 0
            self.current_high = ''
            for i in range(len(self.players)):
                if i == pid:
                    self.players[i].update(0,0,self.current_item)
                    self.last_winner = self.players[i].teamname
                    self.last_item = self.current_item
                    self.current_item = self.itemlist.pop(0)
                else:
                    self.players[i].update(0,0)
            self.bidqueue = []
            self.w.delete("all")
            self.set_podiums(-2)
            self.draw_scoreboard(-2)
            self.shasha_says(self.item_names[self.last_item]+"\n goes to \n"+self.last_winner, 2)
            self.w.update()
        elif bid == -2:
            self.w.delete("all")
            self.set_podiums(-2,pid)
            self.draw_scoreboard(0,pid)
            self.shasha_says("THE WINNER IS\n "+self.players[pid].teamname, 5)
            self.w.update()


if __name__ == "__main__":
    '''EXAMPLE'''
    #Visualizer is created with goal of 3, 2 players and an itemlist
    #v = Visualizer(3,[('Shrivelled Turtleman',120),('White Truffle',150),("john",120),("joe",120),("anna",120),('mark',120),('tom',150),("john",120),("joe",120),("anna",120),("anna",120)],[4,3,3,3,2,1,2,0,3,4])
    #v = Visualizer(5,[('Shrivelled Turtleman',120,'',''),('White Truffle',150,'',''),('White Truffle',150,'','')],[4,3,3,3,2,1,2,0,3,4])
    v = Visualizer(3,[('Blue Dragonfly',120000,'score function','blue_dragonfly.gif'),('Gamma',120000,'Bid one more','gamma.gif'),('SuperShaq',120,'Use the Force','supershaq.gif'),('White Truffle',150,'',''),('Brie',120,'Anything can happen','brie.gif'),('Orange',120,'estimating value',''),('Off by One',120,'Make it rain $$$','off_by_one.gif'),('White Truffle',150,'',''),('Shrivelled Turtleman',120,'',''),('White Truffle',150,'',''),('Shrivelled Turtleman',120,'','')],[4,3,3,3,2,1,2,0,3,4])
    
    
    v.update(0,10,15000) #Player 0, Bid 10, Time used 15
    time.sleep(2)
    v.update(1,10,20000) #Player 1, Bid 10, Time used 20
    time.sleep(2)
    v.update(0,-1) # Player 0 wins the item
    time.sleep(2)
    v.update(1,15,15000) 
    time.sleep(2)
    v.update(0,10,20000)
    time.sleep(2)
    v.update(1,-1)
    time.sleep(2)
    v.update(1,10,20000)
    time.sleep(2)
    v.update(0,10,21000)
    time.sleep(2)
    v.update(1,-1)
    time.sleep(2)
    v.update(1,10,10000)
    time.sleep(2)
    v.update(0,10,15000)
    time.sleep(2)
    v.update(1,-1)
    v.update(1) #Player 0 wins the game

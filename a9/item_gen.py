import random
import argparse

#Parse Arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('nu_diff', metavar='N', type=int,
                   help='The number of different items')
parser.add_argument('list_len', metavar='A', type=int,
                   help='The amount of items')

args = parser.parse_args()

#Open File to write in
item_list = open('itemlist','wb')
rand_list = []

#Create list of numbers
#TODO: Use better seed
random.WichmannHill(10)

for i in range(args.list_len):    
    rand_list.append(random.randint(0,args.nu_diff))

#Shuffle one more time for extra randomness!
random.shuffle(rand_list)

#Write to file
entry = ''
  
for i in rand_list:
  entry += str(i)+" "
  
item_list.write(entry[:-1])
  
item_list.close()
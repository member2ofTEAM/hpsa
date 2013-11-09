import random
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('nu_diff', metavar='N', type=int,
                   help='The number of different items')
parser.add_argument('list_len', metavar='A', type=int,
                   help='The amount of items')

args = parser.parse_args()

item_list = open('itemlist','wb')
rand_list = []

#TODO: Use better seed
random.WichmannHill(10)

for i in range(args.list_len):    
    rand_list.append(random.randint(0,args.nu_diff))
    
random.shuffle(rand_list)
  
for i in rand_list:
  item_list.write(str(i)+" ")
  
item_list.close()
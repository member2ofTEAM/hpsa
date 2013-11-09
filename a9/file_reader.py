import argparse

#Create and Parse arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('itemlist', metavar='list',
                   help='Filename of the Itemlist')
args = parser.parse_args()

#Open file specified from arguments
#And read in files
input = open(args.itemlist)
item_list = input.read()
input.close()

#Create list of items as integers
item_list = item_list.split(" ")
list = []

for item in item_list:
  if item != " ":
    list.append(int(item))

print list
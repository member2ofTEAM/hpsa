import sys

item_list = open(sys.argv[1])
item_list = item_list.read()
item_list.split(" ")

for item in item_list:
  print item," ",
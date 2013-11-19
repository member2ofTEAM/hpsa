import csv
import pdb
import os
from subprocess import Popen
import time

if __name__ == "__main__":
    k = 3
    n = 10
    client_data = {}
    with open('client_data.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            client_data[row[0]] = row[1:]
    for name in client_data:
        root = os.getcwd()
        os.chdir(os.getcwd() + "/" + str(name))
        cmd = client_data[name][0].strip().split(" ")
        Popen(cmd)
        os.chdir(root)


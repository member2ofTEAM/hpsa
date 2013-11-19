#!/bin/bash
p=`wc -l < client_data.csv`
k=$1
n=$2
python server_final.py 1234 $p $k $n 123 0 1

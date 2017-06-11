#!/usr/bin/python
from collections import deque,defaultdict
import os

print "enter path to a folder with logs"
path = raw_input();

customers = defaultdict(list)

for logfile in os.listdir(path):
    print "processing...", logfile

    lines = [line.strip() for line in open(path + "/" + logfile)];
    for line in lines:
        if (line):
            parts = line.split("\t");
            custid = parts[0];
            print "storing customer", custid
            customers[custid].append(logfile);

for (key, value) in customers.items():
    if len(value) > 1:
        print "repeat customer", key

        

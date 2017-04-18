#! /usr/bin/env python

users = {}
print "enter the path of a shadow file:"
myFile = raw_input();
lines = [line.strip() for line in open(myFile)]
for line in lines:
    if (line):
        parts = line.split(":")

        users[parts[0]] = parts[1];

print users;





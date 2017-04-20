#! /usr/bin/env python
#entry = [username,[hashtype,salt,hash],lastchange,etc]

users = {}
print "enter the path of a shadow file:"
myFile = raw_input();
lines = [open(myFile)]
for line in lines:
    if (line):
        parts = line.split(":")
        if parts[1] == "*":
            hash = "*"
        else:
            getpwd = parts[1].split("$")
            hash = getpwd[2]

        users[parts[0]] = hash;

print users;





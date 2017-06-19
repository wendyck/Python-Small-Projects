#! /usr/bin/env python
#entry = [username,[hashtype,salt,hash],lastchange,etc]

import crypt
from passlib.hash import sha512_crypt;
import string
import hashlib

users = {}

cracked = {}

class CrackPasswords(object):
    def __init__(self, file):
        self.name = "cracktactastic passwords found"
        self.file = file;

    def get_pwds(self):
        lines = [line.strip() for line in open(self.file)];
        for line in lines:
            if (line):
                parts = line.split(":");
                username = parts[0];
                getpwd = parts[1].split("$");
                print getpwd;

                if getpwd[1] == "6":
                    hash = getpwd[3];
                    salt = getpwd[2];
                    users[username] = {};
                    users[username]['hash'] = hash;
                    users[username]['salt'] = salt;

    def crack_pwds(self):
        
#All users have a 4 character password using only 1234567890abcdefghijklmnopqrstuvwxyz
#this is clunky :(
        first = range(0,10);
        first.extend(list(string.ascii_lowercase));
        second = range(0,10);
        second.extend(list(string.ascii_lowercase));
        third = range(0,10);
        third.extend(list(string.ascii_lowercase));
        fourth = range(0,10);
        fourth.extend(list(string.ascii_lowercase));

        for user in users.iteritems():            
            username = user[0];
            usalt = user[1]['salt'];
            pwdhash = user[1]['hash'];
            print "Username: %s Salt: %s Hash: %s" % (username, usalt, pwdhash);
            print ("-" * 30);
 
            for i in first:
                #print "checking", i;
                for j in second:
                    for k in third:
                        for l in fourth:
                            text = "";
                            text = str(i) + str(j) + str(k) + str(l);
                            
                            m = hashlib.sha512();
                            m.update(usalt);
                            m.update(text);
                            hashed = m.hexdigest();
                            
                            check = str(hashed);
                            print "."
                            print "checking  %s which crypts to %s" % (text, check);
                            print "."
#check = sha512_crypt.encrypt(text, salt=usalt);

                            if check == pwdhash:
                                print "Match found with %s and %s" % (check, pwdhash);
                                cracked[user] = text;
                                break;
                            else:
                                continue;
                            break;
                        else:
                            continue;
                        break;
                    else:
                        continue;
                    break;
                
        print "finished check for %s - %s" % (username, pwdhash);

#print "enter path to a passwords file"
#file = raw_input();
file = "/Users/wck/git/dumb-python-stuff/homeworks/Homework.txt";
crack = CrackPasswords(file);
crack.get_pwds();
crack.crack_pwds();
print cracked;

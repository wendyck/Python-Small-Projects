#!/usr/bin/python

secret = "butterfly";
print "Welcome to the secret guessing game."
print "Enter a word and I will tell you if it matches my secret."
mystr = raw_input();

if secret == mystr:
    print "you guessed the secret word!"
else:
    print "sorry try again"

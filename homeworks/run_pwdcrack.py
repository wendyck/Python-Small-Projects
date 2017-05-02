#! /usr/bin/env python

import fakemodule.fm
import CrackPasswords.ExtractPw

#this version runs a non-OO version of password cracking functions

print "enter path to a passwords file"
file = raw_input();
print  "enter path to a file to save output to"
outputfile = raw_input();
users = CrackPasswords.ExtractPw.get_pwds(file);
cracked = CrackPasswords.ExtractPw.crack_pwds(users);
CrackPasswords.ExtractPw.save_cleartext(cracked, outputfile);


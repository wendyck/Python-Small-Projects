#! /usr/bin/env python

import fakemodule.fm
import CrackPasswords.CrackPwd

#this version uses an object oriented version of Crack Password

print "enter path to a passwords file"
file = raw_input();
print  "enter path to a file to save output to"
outputfile = raw_input();
crack = CrackPasswords.CrackPwd.CrackPasswords(file);
crack.get_pwds();
crack.crack_pwds();
crack.save_cleartext(outputfile);

#!/usr/bin/python

print "Welcome to calculator. Enter your calculation separated by spaces:";
mystr = raw_input();

if " " in mystr:
    parts = mystr.split(" ");

    operand = parts[1];
    print operand;
    if "+" in operand:
        result = int(parts[0]) + int(parts[2]);
    elif "-" in operand:
        result = int(parts[0]) - int(parts[2]);
    elif "*" in operand:
        result = int(parts[0]) * int(parts[2]);
    elif "/" in operand:
        result = int(parts[0]) / int(parts[2]);
    elif "%" in operand:
        result = int(parts[0]) % int(parts[2]);
    else:
        result = "i'm sorry, i don't understand";

    print result;

else:
    print "run again with spaces, like 1 + 2 "

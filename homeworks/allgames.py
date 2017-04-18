#! /usr/bin/env python

def calculator():
    print "Welcome to calculator. Enter your calculation separated by spaces:";
    mystr = raw_input();

    if " " in mystr:
        parts = mystr.split(" ");

        operand = parts[1];

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
        return result;

def secret(secret_word):
    print "Welcome to the secret guessing game."
    print "Enter a word and I will tell you if it matches my secret."
    mystr = raw_input();

    if secret == secret_word:
        return "you guessed the secret word!"
    else:
        return "sorry try again"

def adventure():
    print "Welcome to Choose Your Adventure. What is your name?"
    name = raw_input();

    print "This is a story about %s. One morning, %s went for a walk. Along the way, %s met a gruffalo. The gruffalo ate %s. The end." % (name, name, name, name)

result = calculator();
print result;

guess = secret("sneakers");
print guess;

adventure();

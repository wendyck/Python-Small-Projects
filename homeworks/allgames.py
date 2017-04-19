#! /usr/bin/env python

def calculator_input():
    print "Welcome to calculator. Enter your calculation separated by spaces:";
    mystr = raw_input();
    operand = ""
    while operand == "":
        if " " in mystr:
            parts = mystr.split(" ");
            operand = parts[1];
            return (int(parts[0]), int(parts[2]), operand);
        else:
            print "Please enter a calculation separated by spaces like 2 + 7"
            mystr = raw_input();
            

def calculator(a,b,operand):

        if "+" in operand:
            result = a + b;
        elif "-" in operand:
            result = a - b;
        elif "*" in operand:
            result = a * b;
        elif "/" in operand:
            result = a / b;
        elif "%" in operand:
            result = a % b;
        else:
            result = "i'm sorry, i don't understand";
        return result;


def secret(secret_word):
    print "Welcome to the secret guessing game."
    print "Enter a word and I will tell you if it matches my secret."
    mystr = raw_input();

    if mystr == secret_word:
        return "you guessed the secret word!"
    else:
        return "sorry try again"

def adventure():
    print "Welcome to Choose Your Adventure. What is your name?"
    name = raw_input();

    print "This is a story about %s. One morning, %s went for a walk. Along the way, %s met a gruffalo. The gruffalo ate %s. The end." % (name, name, name, name)



(a,b,operand) = calculator_input();
result = calculator(a,b,operand);
print result;

guess = secret("sneakers");
print guess;

adventure();

#! /usr/bin/env python
import string
first = range(0,10);
first.extend(list(string.ascii_lowercase));
second = range(0,10);
second.extend(list(string.ascii_lowercase));
third = range(0,10);
third.extend(list(string.ascii_lowercase));
fourth = range(0,10);
fourth.extend(list(string.ascii_lowercase));

for i in first:
    for j in second:
        for k in third:
            for l in fourth:
                
                text = "";
                text = str(i) + str(j) + str(k) + str(l);
                print text;
                if text == "zz79":
                    print "found abcd!!!"
                    print "found abcd!!!"
                    print "found abcd!!!"
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
 
                            

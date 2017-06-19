#!/usr/bin/python
from collections import deque,defaultdict
import os
import re

print "enter path to file"
file = raw_input();
with open(file,'r') as myfiledesc:
    content = myfiledesc.read()

pattern = re.compile(r'<div class=.*?span-6.*?>(.|\n)*?<div class=.*?span-4 last.*?>')
match= pattern.finditer(content)
for m in match:

    print "match found:", m.group(0)


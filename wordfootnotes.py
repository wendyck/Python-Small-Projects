from BeautifulSoup import BeautifulSoup
import sys
import json
import re

#from DC Legal Hackers Communciations Hackathon
# based on https://github.com/adelevie/open-internet-order-footnotes
# 
#turn word doc footnotes.xml in python dict & spit them out
# To get footnotes.xml from docx file:
# rename wordfile.docx to wordfile.docx.zip
# on mac command line, run zip wordfile.docx.zip
# this will make a folder called "word" with "footnotes.xml" inside it
# to run this script: 
# python wordfootnotes.py /path/to/word/footnotes.xml


args = str(sys.argv)
fnFile = sys.argv.pop();

soup=BeautifulSoup(open(fnFile).read())

myFNs = {}
pattern = re.compile(r'supranoteNOTEREF.*?MERGEFORMAT(\d+),')



#print soup.findAll('w:footnote')
fns= soup.findAll('w:footnote')

for footnote in fns:
    id =  int(footnote["w:id"])
    if (id > 0):
        
        #print "Footnote ", id
        #id = footnote.findAll(attrs={"name" : "id"})
        #myID = footnote.findAll('id')
        text = footnote.text
        

        #print text
        if not text.find("NOTEREF") == -1:
            #print "Found NOTEREF in the string."
            match= pattern.finditer(text)
            for m in match:
                #print "found a match" 
                noteLink = m.group(1)
                #print "notelink: ", noteLink
                swap = re.sub(r'supranote.*?MERGEFORMAT(\d+)', r'supra note \1', text)
                #print "swap: ", swap
                myFNs[id] = swap
        else:
            myFNs[id] = text  
            
#print "my footnotes"            
    #print id, notestring     
with open("tmp.txt", "w+") as outputfile:
    for id, notestring in myFNs.items():
         id = str(id)
         notestring = notestring.encode("ascii", errors="ignore")
        
         footnote =  "{0}, {1}\n".format(id, notestring)
         footnote_writeable = footnote
         outputfile.write(footnote_writeable)
        
#create gists
#https://developer.github.com/v3/gists/#create-a-gist
             

# <w:i/> --> italics
# <w:smallCaps/> --> small caps



#f = "footnotes.xml"
#soup=BeautifulSoup(open(f).read())
#print soup.prettify()
# DOESN'T WORK FOR MS WORD
#ids = soup.findAll(attrs={"name" : "id"})
#print soup.findAll(attrs={"name" : "w:footnote"})

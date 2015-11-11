from BeautifulSoup import BeautifulSoup
import sys
import json
import re
from github3 import login
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

fns= soup.findAll('w:footnote')

for footnote in fns:
    id =  int(footnote["w:id"])
    if (id > 0):
        
        footnote_with_tags = footnote.prettify()
 
        cleaner = re.sub(r"<.*?>", "", footnote_with_tags)
        no_newlines = re.sub(r"\n", "", cleaner)
        compact_spaces = re.sub(r"\s{2,}", " ", no_newlines)
        print "??",  compact_spaces

        #print text
        if not compact_spaces.find("NOTEREF") == -1:
            #print "Found NOTEREF in the string."
            match= pattern.finditer(compact_spaces)
            for m in match:
                #print "found a match" 
                noteLink = m.group(1)
                #print "notelink: ", noteLink
                swap = re.sub(r'supranote.*?MERGEFORMAT(\d+)', r'supra note \1', compact_spaces)
                #print "swap: ", swap
                myFNs[id] = swap
        else:
            myFNs[id] = compact_spaces  
            
gistcontent = "#Footnotes in file\n"           
   
for id, notestring in myFNs.items():
        
         id = str(id)
         
         gistcontent += id
         gistcontent += ". "
         gistcontent += notestring 
         gistcontent += "\n"  
         
print gistcontent   
gh = login("wendyck", "")

files = {
    "fn.md" : {
        'content': gistcontent
        }
    }


gist = gh.create_gist('footnotes file from a word doc', files, public=True)
# gist == <Gist [gist-id]>
print(gist.html_url)


#create gists
#https://developer.github.com/v3/gists/#create-a-gist
         
        
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

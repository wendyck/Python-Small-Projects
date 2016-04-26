import re
import sys

import httpagentparser
import collections

def storeDownload(mp3, browser):
    if browser in mp3_downloads_by_browser:
        mp3_downloads_by_browser[browser] += 1;
    else:
        mp3_downloads_by_browser[browser] = 1;  
          
    if mp3 in mp3_downloads:
       mp3_downloads[mp3] += 1;
    else:
       mp3_downloads[mp3] = 1;
        
args = str(sys.argv)
logFile = sys.argv.pop();
pattern = re.compile(r'^([0-9.]+)\s([\w.-]+)\s([\w.-]+)\s(\[[^\[\]]+\])\s"((?:[^"]|\")+)"\s(\d{3})\s(\d+|-)\s"((?:[^"]|\")+)"\s"((?:[^"]|\")+)"$')


#mp3DatePattern = re.compile(r'pkitk.*?(\d{4})(\d{2})(\d{2})', re.I);
mp3DatePattern = re.compile(r'(\d{4})-*(\d{2})-*(\d{2})', re.I);
mp3_downloads = {};              
mp3_downloads_by_browser = {};

lines = [line.strip() for line in open(logFile)]
for line in lines:
    podcastName = "";
    if (line):
        #print line;
        match= pattern.finditer(line)
        for m in match: 
           
           useragent = m.group(9)
           request = m.group(5)
           ref = m.group(7)
           if ( re.search("GET.*?podcast.*?\.mp3 ", request, re.I)):
    
               mp3File = request.replace("GET /assets/uploads/podcasts/", "");
               mp3File = mp3File.replace("podcasts/", "");
               mp3File = mp3File.replace(" HTTP/1.1", "");
               mp3File = mp3File.replace("GET /files/","");
    
               #dateMatch = mp3DatePattern.match(mp3File);
               if (re.search(mp3DatePattern, mp3File)):
                   dateMatch= mp3DatePattern.search(mp3File);
                   year = dateMatch.group(1);
                   month = dateMatch.group(2);
                   day = dateMatch.group(3);
               
                   podcastName = year + "-" + month + "-" + day;
               else:    
                   podcastName = mp3File;
                   
               if (re.search("itunes", useragent, re.I) ):
                  storeDownload(podcastName, "iTunes");
                 
               elif (re.search(".*?bot", useragent, re.I) or re.search("Crawler", useragent, re.I)):
                   storeDownload(podcastName, "bot");
               else: 
                   agent = httpagentparser.simple_detect(useragent);
                   os = agent[0];
                   browser = agent[1];
                   
                   if re.search("unknown", os, re.I):
                       simplestring = browser;
                   else:
                       simplestring = os;          
                       if (re.search("^ip", simplestring, re.I) or re.search("Windows Phone", simplestring, re.I)):
                           simplestring = "Mobile OS"
                       elif (re.search("Windows", simplestring, re.I) or re.search("MacOS", simplestring, re.I)):
                           simplestring = "Desktop Browser"
                   storeDownload(podcastName, simplestring);               
                       
totalDownloads = 0;  

print "Total Downloads by Browser";      
for browser, count in sorted(mp3_downloads_by_browser.items()):
    print browser, ":", count;
         
print "Downloads by Podcast file";              
for file, count in sorted(mp3_downloads.items(), reverse=True):
    totalDownloads += count;
    print "\t", file, ":", count;
        
print "Total Downloads: ", totalDownloads;        
    
                      
#!/usr/bin/python

import json
import urllib2
import re



def lookupByUsername(userID):
    urltemplateByUsername = "https://www.googleapis.com/youtube/v3/channels?key=[KEY]&part=statistics&forUsername="
    myreq = urltemplateByUsername + userID;
    print myreq;
    doLookup(myreq);

def lookupByChannelID(channel):
    urltemplateByChannelID = "https://www.googleapis.com/youtube/v3/channels?key=[KEY]&part=statistics&part=statistics&id="
    myreq = urltemplateByChannelID + channel;
    print myreq;
    doLookup(myreq);

def doLookup(urlToUse):
    global viewcount;
    global vidcount;
    # Send the GET request
    try:
        req = urllib2.Request(urlToUse, None, {})
        # Read the response
        resp= urllib2.urlopen(req).read();
        #small change
        # Interpret the JSON response
        data = json.loads(resp.decode('utf8'));
        
        for item in data['items']:
            myViewCount =  int(item['statistics']['viewCount']);
            viewcount += myViewCount;
            myVidCount = int(item['statistics']['videoCount']);
            vidcount += myVidCount;
            print "view count: %s"  % myViewCount;
            print "video count: %s " %  myVidCount;

    except: # catch *all* exceptions
        print "error";


#f=open('/Users/wck/Documents/PK/vidcount/youtube.txt','r')
#for line in f.readline():


viewcount = 0;
vidcount = 0;
print viewcount;
print vidcount;

myFile ='/Users/wck/Documents/PK/urls2.txt';

lines = [line.strip() for line in open(myFile)]
for line in lines:
    if (line):
        print line;
        m = re.search(r"youtube.com/(.*)", line)
        if m:
            
            #we should either have short url, or /user/ or /channel/
            urlTail = m.groups()[0];
            if "user/" in urlTail:
                
                n = re.search(r"user/(.*)", m.groups()[0])
                if n:
                    
                    #we should have a username
                    ytUsername = n.groups()[0];
                    lookupByUsername(ytUsername);

            elif "channel/" in urlTail:
                cid = re.search(r"channel/(.*)", m.groups()[0])
                if cid:
                    
                    channelID = cid.groups()[0];
                    lookupByChannelID(channelID);
            else:
             
                lookupByUsername(urlTail);

print viewcount;
print vidcount;

print "view count: %s"  % viewcount;
print "video count: %s " %  vidcount;



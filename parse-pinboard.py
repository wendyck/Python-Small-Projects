#!/usr/bin/python

import json
import urllib2
import sys
import argparse
import datetime

def doLookup(urlToUse):
    january = "January\n";
    feb = "February\n";
    march = "March\n";
    april = "April\n";
    may = "May\n";
    june = "June\n";
    july = "July\n";
    august = "August\n";
    september = "September\n";
    october = "October\n";
    november = "November\n";
    december = "December\n";

    req = urllib2.Request(urlToUse, None, {})
    # Read the response
    resp= urllib2.urlopen(req).read();

    # Interpret the JSON response
    data = json.loads(resp.decode('utf8'));
   
    
    for item in data:

        bookmark_url = item['href'];
        text = item['description'];
        date = item['time'];
        
        if (date.startswith(year)):
            mytext = bookmark_url+ "\n"+ text+"\n"+  date+ "\n---------------\n";
            if (date.startswith(year + "-01")):
                january = january + mytext;
                
            elif (date.startswith(year + "-02")):
                feb = feb + mytext; 
            elif (date.startswith(year + "-03")):
                march = march + mytext;
            elif (date.startswith(year + "-04")):
		april = april + mytext;
            elif (date.startswith(year + "-05")):
		may = may + mytext;
            elif (date.startswith(year + "-06")):
		june = june + mytext;
            elif (date.startswith(year + "-07")):
		july = july + mytext;
            elif (date.startswith(year + "-08")):
		august = august + mytext;
            elif (date.startswith(year + "-09")):
		september = september + mytext;
            elif (date.startswith(year + "-10")):
		october = october + mytext;
            elif (date.startswith(year + "-11")):
		november = november + mytext;
            elif (date.startswith(year + "-12")):
		december = december + mytext;
                
    print january;
    print feb;
    print march;
    print april;
    print may;
    print june;
    print july;
    print august;
    print september;
    print october;
    print november;
    print december;
    
    
myKey = "&auth_token=";
myTag = "&tag=";
myrootURL = "https://api.pinboard.in/v1/posts/all?format=json";

parser = argparse.ArgumentParser(description='Generate Simple Text Output of Pinobard Tag by Month')

parser.add_argument('-t','--tag', 
                    help='call with tag to fetch all pins with a tag');

parser.add_argument('-a','--apikey',
                    help='call with apikey to supply a pinboard api key to use. get your pinboard api key at https://pinboard.in/settings/password');

parser.add_argument('-y','--year',
                    help='call with year to print tags for a year. default is current year.');


args = parser.parse_args();
tagText = "";
apiText = "";

now = datetime.datetime.now();
year =  str(now.year);

if (args.tag and args.apikey):
    tagText = args.tag;
    apiText = args.apikey;
    myURL = myrootURL + myTag + tagText + myKey + apiText;
    print myURL;

    if args.year:
        year = args.year;
    doLookup(myURL);

                  
else:
    parser.print_help()   



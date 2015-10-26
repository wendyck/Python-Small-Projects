import requests
import sys


def checkURL(companyurl):
   
    companyurl = "http://" + companyurl;
    r = requests.get(companyurl)
    print companyurl, ",", r.status_code


args = str(sys.argv)
myFile = sys.argv.pop();

lines = [line.strip() for line in open(myFile)]
for line in lines:
    if (line):
        #print line;
        checkURL(line);
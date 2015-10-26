import urllib2, urllib
import sys

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):     
    def http_error_301(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_301( 
            self, req, fp, code, msg, headers)              
        result.status = code                                 
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):   
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)              
        result.status = code                                
        return result                                       



def checkURL(companyurl):
   
    companyurl = "http://" + companyurl;
    try:
        req = urllib2.Request(companyurl, None, {})
        # Read the response
        
        response = urllib2.urlopen(req).read();
        #print response
        try:
            print companyurl, ",", response.getcode;
        except:
                print "error" 
                      
    except urllib2.HTTPError as e:
        print companyurl,",", e.code
        #print e.read() 
        



args = str(sys.argv)
myFile = sys.argv.pop();
opener = urllib2.build_opener(SmartRedirectHandler())
urllib2.install_opener(opener)

lines = [line.strip() for line in open(myFile)]
for line in lines:
    if (line):
        #print line;
        checkURL(line);
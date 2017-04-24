import argparse
import urllib2
parser = argparse.ArgumentParser(description='check IPs in Firewall Log')
parser.add_argument('-f','--file', 
                    help='call with file to run')

args = parser.parse_args();

if args.file:
    mydict = {}
    filename = args.file;

    with open(filename, "r") as ins:
    #array = []
        for line in ins:
            mylist = line.split(',')

            key = mylist[14] + ":" + mylist[20]
            if key in mydict:
                mydict[key] += 1;
            else:    
                mydict[key] = 1;
    for w in sorted(mydict, key=mydict.get, reverse=True):
        print key, "appears", mydict[w], "times"
        ips = w.split(':');
        source=ips[0].strip('"');
        destination=ips[1].strip('"');
        #print source, destination
        if "10.50.2" not in source:
            myurl = 'http://ipinfo.io/' + source + "/country";

            try:
                response = urllib2.urlopen(myurl)
                json = response.read()
                print json
            except:
                print "error on lookup of", source

        
        if "10.50.2" not in destination:
            myurl2 = 'http://ipinfo.io/' + destination + "/country";

            try:
                responsed = urllib2.urlopen(myurl2)
                jsond = responsed.read()
                print jsond
            except:
                print "error on lookup of", destination

#    with file(filename) as f:
#        s = f.read();

    #print s;

else:
    parser.print_help()

#!/usr/bin/python

urls = ['http://www.one.com', 'http://www.two.com', 'http://www.three.com', 'http://www.four.com', 'http://www.two.com', 'http://www.three.com', 'http://www.four.com'];
cache = dict();

tmp = "";

size = len(urls)

for i, url in enumerate(urls):
   
    tmp = "";
    cache[url] = i;
    
    if ((i+1) == size):
       
        #last item in list
        tmp = urls[i-1];
        tmp += url;
    elif ((i > 1) and (i < size)):
        tmp = urls[i-1];
        tmp += url;
        tmp += urls[i+1];
    
    else:
        tmp = url + urls[i + 1];
          
    if tmp in cache.keys():
        print "repeated url set", tmp;
        exit;
    else: 
        cache[tmp] = i;
  

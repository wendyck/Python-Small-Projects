import sys
import argparse
import json
import requests
import time
from datetime import datetime, timedelta
from tabulate import tabulate

start_date = "";
end_date = "";

json_data=open('config.json');
configData = json.load(json_data);    
json_data.close();  
client_id = configData["client_id"];
client_secret = configData["client_secret"];
gID = configData["google_analytics_id"];

    
def checkForNewAuthorization(device_code):

    headers = { 'Content-Type' : 'application/x-www-form-urlencoded' };
    url = 'https://accounts.google.com/o/oauth2/token';
    values = {'client_id' : client_id,
              'grant_type' : "http://oauth.net/grant_type/device/1.0",
              'client_secret' :  client_secret, 
              'code' : device_code }

    r = requests.post(url, headers=headers, data=values);
    response = r.json();
    
    if  response.has_key("access_token"):
        storeAuthorization(response);
        return response;
    else:
        if response.has_key("error"):
            print response["error"];
        return {};
 
def generateAuthCodeRequest():

    headers = { 'Content-Type' : 'application/x-www-form-urlencoded' };
    url = 'https://accounts.google.com/o/oauth2/device/code';
    values = {'client_id' : client_id,
          'scope' : 'email profile https://www.googleapis.com/auth/analytics.readonly' }

    r = requests.post(url, params=values)
    response = r.json();
    print "   " * 20;
    print "   " * 20;  
    print "Open", response['verification_url'], "in a web browser and enter", response['user_code'];
    print "   " * 20; 
    print "   " * 20; 
       
    authenticated = False;
    time.sleep(5);
    print "checking if authenticated yet";
    while not(authenticated):
        authResponse = checkForNewAuthorization(response['device_code']);
        if  authResponse.has_key("access_token"):
            authenticated = True;
            print "   " * 20; 
            print "User authentication now stored."
            print "   " * 20; 
        else:
            time.sleep(5);
    
    return authResponse;

def storeAuthorization(authTokens):
    with open('auth.txt', 'w') as outfile:
        json.dump(authTokens, outfile);
    
      
         
def getAuthorizationFromFile():
      json_data=open('auth.txt');
      data = json.load(json_data);
      json_data.close();  
      return data; 

def fetchAndPrintSummary(authTokens, values, title): 
    analyticsResponse = fetchData(authTokens, values);   
    print "   " * 20; 
    print "   " * 20;  
          
    print title, analyticsResponse["profileInfo"]["profileName"], "for date range", start_date, "to", end_date;
    for metric in analyticsResponse["totalsForAllResults"]:
            print metric, ":", analyticsResponse["totalsForAllResults"][metric];
    print "   " * 20;  
    print "   " * 20;    

def fetchAndPrintTable(authTokens, values, title): 
    analyticsResponse = fetchData(authTokens, values);
   
    print "   " * 20;
    print "   " * 20;             
    print title, analyticsResponse["profileInfo"]["profileName"], "for date range", start_date, "to", end_date;
    columnHeaders = [];
    for entry in analyticsResponse["columnHeaders"]: 
        columnHeaders.append(entry["name"]);              
    print tabulate(analyticsResponse["rows"], headers=columnHeaders);
    print "   " * 20;
    print "   " * 20; 
         
        
def fetchData(authTokens, values):
    token = 'Bearer ' + authTokens["access_token"];
    headers = {'Authorization':  token};
    url = "https://www.googleapis.com/analytics/v3/data/ga";
    r = requests.get(url, headers=headers, params=values);
    analyticsResponse = r.json();
    if  analyticsResponse.has_key("error"):
            if "Invalid Credentials" in analyticsResponse["error"]["message"]:
                print "   " * 20; 
                print "   " * 20; 
                print "Please refresh your credentials by re-running with --begin (or -b) option";
                print "   " * 20; 
                print "   " * 20; 
                return;
    return analyticsResponse;     
        
         
        
def getDates():
    if args.startDate:
         
        start_date = args.startDate;
            
    if args.endDate:
         
        end_date = args.endDate;
    else:
        
        now = datetime.now();
        yesterday = datetime.now() + timedelta(days = -1);
        padded_ymonth = "%02d" % (yesterday.month,)
        padded_nmonth = "%02d" % (now.month,)
        padded_yday = "%02d" % (yesterday.day,)
        padded_nday = "%02d" % (now.day,)
        
        start_date = str(yesterday.year) + "-" + str(padded_ymonth) + "-" + str(padded_yday);
        end_date = str(now.year) + "-" + str(padded_nmonth) + "-" + str(padded_nday);
        print "Will run with default last 24 hours", start_date, "to", end_date;
        print "To set a date, run with -s YYYY-MM-DD and -e YYYY-MM-DD"; 
        
    return (start_date, end_date);         


parser = argparse.ArgumentParser(description='Generate Simple Analytics Report')

parser.add_argument('-b','--begin', action='store_true',
                    help='Call with begin if you need to generate an authorization URL and Token as your first step') # boolean arg

parser.add_argument('-sc','--social', action='store_true',
                    help='Call with social to generate metrics for referrals from social networks. You can also set a start and end date') # boolean arg


parser.add_argument('-r','--report', action='store_true',
                    help='Call with report to generate a summary traffic report. You can also set a start and end date') # boolean arg

parser.add_argument('-k','--keywordreport', action='store_true',
                    help='Call with keywordreport to generate a keyword report. You can also set a start and end date') # boolean arg

parser.add_argument('-rf','--referralreport', action='store_true',
                    help='Call with referralreport to generate a referral traffic report. You can also set a start and end date') # boolean arg
parser.add_argument('-m','--mobilereport', action='store_true',
                    help='Call with mobilereport to generate a mobile traffic report. You can also set a start and end date') # boolean arg
parser.add_argument('-md','--mobilereportbydevice', action='store_true',
                    help='Call with mobilereportbydevice to generate a mobile traffic report by device. You can also set a start and end date') # boolean arg
parser.add_argument('-u','--userreport', action='store_true',
                    help='Call with userreport to generate number of new sessions vs returning sessions. You can also set a start and end date') # boolean arg
parser.add_argument('-bo','--browserreport', action='store_true',
                    help='Call with browserreport to generate breakdown of sessions by  Operating System & web browser. You can also set a start and end date') # boolean arg

parser.add_argument('-tos','--timeonsitereport', action='store_true',
                    help='Call with timeonsitereport to generate number of sessions and total time on site. You can also set a start and end date') # boolean arg

parser.add_argument('-tr','--alltrafficsourcesreport', action='store_true',
                    help='Call with alltrafficsourcesreport to generate site usage data broken down by source and medium, sorted by sessions in descending order. You can also set a start and end date') # boolean arg
parser.add_argument('-rs','--referringsitesreport', action='store_true',
                    help='Call with referringsitesreport to generate list of domains and how many sessions each referred to your site, sorted by pageviews in descending order. You can also set a start and end date') # boolean arg

parser.add_argument('-se','--searchenginesreport', action='store_true',
                    help='Call with searchenginesreport to generate list of domains and how many sessions each referred to your site, sorted by pageviews in descending order. You can also set a start and end date') # boolean arg
parser.add_argument('-seo','--searchenginesorganicreport', action='store_true',
                    help='Call with searchenginesorganicreport to generate site usage data for organic traffic by search engine, sorted by pageviews in descending order. You can also set a start and end date') # boolean arg
parser.add_argument('-tc','--topcontentreport', action='store_true',
                    help='Call with topcontentreport to generate most popular content, sorted by most pageviews. You can also set a start and end date') # boolean arg
parser.add_argument('-tlp','--toplandingpagereport', action='store_true',
                    help='Call with toplandingpagereport to generate most popular landing page, sorted by most pageviews. You can also set a start and end date') # boolean arg
parser.add_argument('-week','--weeklyemailreport', action='store_true',
                    help='Call with weeklyemailreport to generate data for email report. You can also set a start and end date') # boolean arg

parser.add_argument('-pg','--pagepath', action='store_true',
                    help='Call with pagepath to generate data for {}. You can also set a start and end date') # boolean arg


parser.add_argument('-tpp','--timeperpagereport', action='store_true',
                    help='Call with timeperpagereport to generate metrics for time per page. You can also set a start and end date') # boolean arg

parser.add_argument('-s','--startDate', 
                    help='Call with startDate and a date in format YYYY-MM-DD') # boolean arg

parser.add_argument('-e','--endDate', 
                    help='Call with startDate and a date in format YYYY-MM-DD') # boolean arg



args = parser.parse_args();


if args.begin:                       
     
    generateAuthCodeRequest();
    

if args.report:
    (start_date, end_date) = getDates();    
    authTokens = getAuthorizationFromFile();
    values = {'ids' : gID,
              'start-date' : start_date,
              'end-date' : end_date,
              'metrics' : 'ga:sessions,ga:bounces,ga:avgSessionDuration'};
    fetchAndPrintSummary(authTokens, values, "Page Views Summary");
    
    #daily visits/percentage of new visits for dates
    values = {'ids' : gID,
              'dimensions' : "ga:date",
              'metrics' : 'ga:visits,ga:visitors,ga:percentNewVisits, ga:pageviews',
              'start-date' : start_date,
               'end-date' : end_date};
    fetchAndPrintTable(authTokens, values, "Daily Traffic Summary");

elif args.social:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
               'dimensions' : 'ga:socialNetwork',
                  'metrics' : 'ga:visitors,ga:pageviews,ga:percentNewVisits, ga:visits',
                  'max-results' : "100",
                  'start-date' : start_date,
                  'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Social ");
        
    
elif args.keywordreport:    
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
              'dimensions' : "ga:keyword",
              'metrics' : 'ga:sessions',
              'max-results' : "1000",
              'sort' : '-ga:sessions',
              'start-date' : start_date,
              'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Keyword Report");     
    
elif args.referralreport:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                  'dimensions' : "ga:fullReferrer",
                  'metrics' : 'ga:visits,ga:visitors,ga:percentNewVisits, ga:pageviews,ga:avgTimeOnPage',
                  'max-results' : "100",
                  'sort' : '-ga:pageviews',
                  'start-date' : start_date,
                  'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Referrals Report");             

elif args.mobilereport:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                  'dimensions' : "ga:source,ga:medium",
                  'metrics' : 'ga:sessions,ga:pageviews,ga:sessionDuration,ga:bounces',
                  'max-results' : "100",
                  'start-date' : start_date,
                  'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Mobile Report");
     
elif args.mobilereportbydevice:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                  'dimensions' : "ga:mobileDeviceInfo,ga:source",
                  'metrics' : 'ga:sessions,ga:pageviews,ga:sessionDuration,ga:bounces',
                  'segment' : 'gaid::-14',
                  'max-results' : "100",
                  'start-date' : start_date,
                  'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Mobile Report");
     
elif args.userreport:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                  'dimensions' : "ga:userType",
                  'metrics' : 'ga:sessions,ga:pageviews,ga:sessionDuration,ga:avgTimeOnPage',
                  'start-date' : start_date,
                  'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "User Report");

elif args.timeperpagereport:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
               'dimensions' : "ga:source,ga:medium,ga:pagePath",
               'metrics' : 'ga:timeOnPage',
               'max-results' : "100",
               'sort' : '-ga:timeOnPage',
               'start-date' : start_date,
               'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Time on Pages Report"); 

elif args.browserreport:         
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                  'dimensions' : "ga:operatingSystem,ga:operatingSystemVersion,ga:browser,ga:browserVersion",
                  'metrics' : 'ga:sessions,ga:percentNewVisits, ga:pageviews',
                  'sort' : '-ga:sessions',
                  'max-results' : "100",
                  'start-date' : start_date,
                  'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Browser and OS Report");
     
elif args.timeonsitereport:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
              'metrics' : 'ga:sessions,ga:sessionDuration,ga:avgTimeOnPage,ga:uniquePageviews',
              'start-date' : start_date,
              'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Time on Site Report");     
           
     
elif args.alltrafficsourcesreport:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : configData["google_analytics_id"],
                'dimensions' : "ga:source,ga:medium",
                'metrics' : 'ga:sessions,ga:pageviews,ga:sessionDuration,ga:exits',
                'sort' : '-ga:sessions',
                'max-results' : "100",
                'start-date' : start_date,
                'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Traffic Sources Report");
    
         
     
elif args.referringsitesreport:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                'dimensions' : "ga:source",
                'metrics' : 'ga:pageviews,ga:sessionDuration,ga:exits',
                'filters' : 'ga:medium==referral',
                'sort' : '-ga:pageviews',
                'max-results' : "100",
                'start-date' : start_date,
                'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Referring Sites Report");
 
elif args.searchenginesreport:         
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                'dimensions' : "ga:source",
                'metrics' : 'ga:pageviews,ga:sessionDuration,ga:exits',
                'filters' : 'ga:medium==cpa,ga:medium==cpc,ga:medium==cpm,ga:medium==cpp,ga:medium==cpv,ga:medium==organic,ga:medium==ppc',
                'sort' : '-ga:pageviews',
                'max-results' : "100",
                'start-date' : start_date,
                'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Search Engine Traffic Report");
     
     
elif args.searchenginesorganicreport:     
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                'dimensions' : "ga:source",
                'metrics' : 'ga:pageviews,ga:sessionDuration,ga:exits',
                'filters' : 'ga:medium==organic',
                'sort' : '-ga:pageviews',
                'max-results' : "100",
                'start-date' : start_date,
                'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Search Engines Organic Traffic Report");             

elif args.topcontentreport:     
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                'dimensions' : 'ga:pagePath',
                'metrics' : 'ga:pageviews,ga:uniquePageviews,ga:timeOnPage,ga:bounces,ga:entrances,ga:exits',
                'sort' : '-ga:pageviews',
                'max-results' : "100",
                'start-date' : start_date,
                'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Top Content Report");
     
elif args.toplandingpagereport:
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
                'dimensions' : 'ga:landingPagePath',
                'metrics' : 'ga:entrances,ga:bounces',
                'sort' : '-ga:entrances',
                'max-results' : "100",
                'start-date' : start_date,
                'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Top Landing Pages Report");              
     
elif args.weeklyemailreport:      
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
               'metrics' : 'ga:pageviewsPerSession,ga:users,ga:bounceRate,ga:sessions,ga:uniquePageviews,ga:pageviews,ga:avgSessionDuration',
               'start-date' : start_date,
               'end-date' : end_date};
     fetchAndPrintSummary(authTokens, values, "Weekly Summary");
     
     
     values = {'ids' : gID,
               'dimensions' : "ga:fullReferrer",
               'metrics' : 'ga:visits,ga:visitors,ga:percentNewVisits, ga:pageviews',
               'max-results' : "10",
               'start-date' : start_date,
               'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Top 10 Referrals");
     
     
     values = {'ids' : gID,
               'dimensions' : 'ga:landingPagePath',
               'metrics' : 'ga:entrances,ga:bounces',
               'sort' : '-ga:entrances',
               'max-results' : "10",
               'start-date' : start_date,
               'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Top 10 Landing Pages");
     
elif args.pagepath:     
     (start_date, end_date) = getDates();
     authTokens = getAuthorizationFromFile();
     values = {'ids' : gID,
               'dimensions' : 'ga:pagePathLevel1,ga:fullReferrer',
               'metrics' : 'ga:visitors,ga:pageviews',
               'max-results' : "100",
               'start-date' : start_date,
               'end-date' : end_date};
     fetchAndPrintTable(authTokens, values, "Pages on Site");
                 
else:
    parser.print_help()                 # or print help

    

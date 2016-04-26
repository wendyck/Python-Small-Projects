from twilio.rest import TwilioRestClient
import MySQLdb as mdb
import sys
import json
from datetime import datetime, timedelta
import us


#read in configuration
json_data=open('apidata.json');
data = json.load(json_data)

json_data.close()

# Your Account Sid and Auth Token from twilio.com/user/account
accountSid = data["twilio"]["accountSid"]
authToken = data["twilio"]["authToken"];
myNumber = data["twilio"]["fromNumber"];

client = TwilioRestClient(accountSid, authToken)


class Campaign(object):
    sms = ""
    id = 0
    sendDate = ""
    sendTime = ""
    unixSend = ""
    
    
class Subscriber(object):
    userid = 0
    number = ""
    state = ""
    lat =""
    long= ""
 
  
def insertSet(sql):
  
        try:
            con = mdb.connect(data["database"]["host"], data["database"]["user"], data["database"]["password"], data["database"]["database"]);
            with con:
                cur = con.cursor(mdb.cursors.DictCursor)
                cur.execute(sql)
                rows = cur.fetchall()
                
                return rows;    
        except mdb.Error, e:  
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
    
        finally:         
            if con:
                con.close()
                    
def selectSet(sql):
        try:
            con = mdb.connect(data["database"]["host"], data["database"]["user"], data["database"]["password"], data["database"]["user"]);
            with con:
                cur = con.cursor(mdb.cursors.DictCursor)
                cur.execute(sql)
                rows = cur.fetchall()
                
                return rows;    
        except mdb.Error, e:  
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
    
        finally:         
            if con:
                con.close()
        
def findTargetsForCampaign(id):
    targets = "select * from campaign_target_sets cts, target_sets ts where cts.target_set_id = ts.id and cts.alert_id = " + str(id);
  
    targetSet = selectSet(targets);
    for row in targetSet:
      print "for campaign ", row["alert_id"], " geo target ",  row["geo_target"];
    return targetSet;  
 
def getSubscribersForGeo(geoArea):
    # todo
    # special case for geo area 00
    subscribers = "select * from subscriber where status = 1";
    if (geoArea != "00"):                        
         subscribers = subscribers + " and state = '" + geoArea + "'";  
     
    #print subscribers;
    subscriberSet = selectSet(subscribers); 
    return subscriberSet;
      
def findUpcoming():
    
  upcoming = "SELECT id,sms, send, DATE(FROM_UNIXTIME(`send`)) as date, TIME(FROM_UNIXTIME(`send`)) as time FROM alert WHERE DATE(FROM_UNIXTIME(`send`)) >= DATE(NOW()) and status = 0 order by DATE(FROM_UNIXTIME(`send`))";  
  rows = selectSet(upcoming)

  return rows;    

def insertSent(sid, campaign_id, user_id):

    insertSentStatus = "insert into sent (user_id, alert_id, status, sid)  \
      VALUES ('%d', '%d', '%d', '%s')" % \
       ( user_id, campaign_id, 0, sid);
    
    print insertSentStatus;
    rows= selectSet(insertSentStatus);
    print rows;


def sendSMSViaTwilio(message, toNumber, fromNumber):
    
    mysid = client.messages.create(body=message,
                                     to=toNumber,    
                                     from_=fromNumber) 
    
    return mysid;
    
def campaignTimeWindowCheck(campaign):
    # datetime.datetime.now().time()
    now = datetime.now();
    campaignStartTime = datetime.fromtimestamp(int(campaign.unixSend))
    
    print "now: ", now, " campaign time ", campaignStartTime
    
    if (campaignStartTime < now):
        print "campaignStartTime < now";
        return True;
    else:
        print "Will not send yet because campaignStartTime is later than current time"
        return False;
    
    
        
    
def subscriberTimeWindow(campaign, subscriber):
     
     nowTime = datetime.now().time();
     subState = us.states.lookup(subscriber.state);
     subTimeZone = subState.time_zones[0];
   
     print "timezone is " + subTimeZone;

     if "New_York" in subTimeZone:
         print "eastern time zone for  ",  subscriber.userid;
         campaignStartTime = datetime.fromtimestamp(int(campaign.unixSend));
         campaignTime = campaignStartTime.time();
         if (nowTime > campaignTime):
             print "can send ", campaign.id, " because ", nowTime, " > ", campaignTime; 
             return True;
         
     elif "Chicago" in subTimeZone:
         
         campaignStartTimeCentral = datetime.fromtimestamp(int(campaign.unixSend)) + timedelta(hours=1);
         print "*** Subscriber ",  subscriber.userid,  " in Central time, campaign should send at ",  campaignStartTimeCentral.time();
         if (nowTime > campaignStartTimeCentral.time()):
            print "can send ", campaign.id, " because ", nowTime, " > ", campaignStartTimeCentral.time(); 
            return True;
        
     elif "Denver" in subTimeZone:
         campaignStartMountain = datetime.fromtimestamp(int(campaign.unixSend)) + timedelta(hours=2);
         print "*** Subscriber ",  subscriber.userid,  " in Mountain time, campaign should send at ",  campaignStartMountain.time();
         if (nowTime > campaignStartMountain.time()):
            print "can send ", campaign.id, " because ", nowTime, " > ", campaignStartMountain.time(); 
            return True;
        
     else:
         campaignStartTimePacific = datetime.fromtimestamp(int(campaign.unixSend)) + timedelta(hours=3);
         print "*** Subscriber ",  subscriber.userid,  " in Pacific time, campaign should send at ",  campaignStartTimePacific.time();
         if (nowTime > campaignStartTimeCentral.time()):
            print "can send ", campaign.id, " because ", nowTime, " > ", campaignStartTimePacific.time(); 
            return True;
     
    

def checkAlertSentForSubscriber(campaign, subscriber):
     already_sent = "select * from sent where alert_id =" + str(campaign.id) + " and user_id = " + str(subscriber.userid);
     print already_sent;
     rows = selectSet(already_sent);
     print "returned ", rows;
     if (len(rows)>1):
         return True;
     else:
         return False;

def sendAlertToSubscriber(campaign, subscriber):
 
    sentSid = sendSMSViaTwilio(campaign.sms, subscriber.phoneNumber, myNumber);
    insertSent(sentSid, campaign.id, subscriber.userid);


campaigns = findUpcoming();
for row in campaigns:
    print "campaign: ", row["id"], row["sms"], row["date"], row["time"], row["send"]
    alert_id = row["id"];
    
    campaignToSend = Campaign()
    campaignToSend.id = row["id"]
    campaignToSend.sms =  row["sms"]
    campaignToSend.sendDate = row["date"]
    campaignToSend.sendTime = row["time"]
    campaignToSend.unixSend = row["send"]
    if (campaignTimeWindowCheck(campaignToSend)):
       #in time window
        t = findTargetsForCampaign(alert_id);
        for targetSet in t:
            print "----------------------------------------"
            #print "target set id: ", targetSet["id"], " geo target ", targetSet["geo_target"]
            geoSet = getSubscribersForGeo(targetSet["geo_target"]);
            for subscriber in geoSet:
                #print "subscriber phone #", subscriber["number"], " will be sent alert ",  campaignToSend.id;
                subscriberToSend = Subscriber()
                subscriberToSend.userid = subscriber["user_id"]
                subscriberToSend.phoneNumber = subscriber["number"]
                subscriberToSend.state = subscriber["state"]
                subscriberToSend.lat = subscriber["lat"]
                subscriberToSend.long = subscriber["long"]
                if (subscriberTimeWindow(campaignToSend, subscriberToSend)):
                    #check to see if there is a sent table entry for this subscriber & campaign
                    if (not(checkAlertSentForSubscriber(campaignToSend, subscriberToSend))):
                        sendAlertToSubscriber(campaignToSend, subscriberToSend);
                        print "will send to subscriber ", subscriberToSend.userid;
                        print "===================================================="
                    else:
                        print "Can't send to subscriber ", subscriberToSend.userid;
                        print "===================================================="
                else:
                    print "===================================================="

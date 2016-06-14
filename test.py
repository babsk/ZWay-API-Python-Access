import requests
import json
import login
import schedule

def displaySchedule (d):
    numEvents = len(d)
    for i in range (0, numEvents):
        msg = ""
        msg += str(d[i]['id'])
        msg += " day: "
        msg += str(d[i]['day'])
        msg += " time: "
        msg += str(d[i]['hour'])
        msg += "."
        msg += str(d[i]['minute'])
        msg += " sp: "
        msg += str(d[i]['sp'])
        print (msg)    

def processData (d): 
    o = json.loads(d)

    numTimers = len(o['objTimer'])
    print ("num timers is " + str(numTimers))

    for i in range (0, numTimers):
        msg = ""
        msg += " day: " + str(o['objTimer'][i]['iDay'])
        msg += " time: " + str(o['objTimer'][i]['iTm'])
        msg += " sp: " + str(o['objTimer'][i]['fSP'])
        print (msg)
                    

roomid = int(input ("Enter id of room: "))


#data = input ("Enter heatgenius schedule: ")
#print (data)

#processData (data)

cookie = login.send()
r = schedule.get_schedule (cookie,roomid)

displaySchedule (r.json()['data'])

print ("Enter new trigger point:")
day = int(input ("Day: "))
hour = int(input ("Hour: "))
minute = int (input ("Minute: "))
sp = int (input ("SP: "))

trigger = {'day': day, 'id': '***', 'minute': minute, 'hour': hour, 'eventName': '****', 'active': False, 'sp': sp}
sched = r.json()['data']
sched.append(trigger)

data = {"data":sched}
r = schedule.set_schedule(cookie,roomid,data)

r = schedule.get_schedule(cookie,roomid)
displaySchedule (r.json()['data'])

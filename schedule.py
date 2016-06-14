import requests
import json
import login

schedule_url = login.api+"hillview/schedule/"

def get_schedule (cookie,id):
    
    # request the schedule
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    r = requests.get(schedule_url+str(id),headers=headers)

    return r

def set_schedule (cookie,id,payload):

    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now set the schedule
    r = requests.post(schedule_url+str(id),data=json.dumps(payload),headers=headers)
    

if __name__ == "__main__":

    cookie = login.send()
    r = get_schedule(cookie,3)

    # display the schedule

    numEvents = len(r.json()['data'])
    for i in range (0, numEvents):
        msg = ""
        msg += str(r.json()['data'][i]['id'])
        msg += " day: "
        msg += str(r.json()['data'][i]['day'])
        msg += " time: "
        msg += str(r.json()['data'][i]['hour'])
        msg += "."
        msg += str(r.json()['data'][i]['minute'])
        msg += " sp: "
        msg += str(r.json()['data'][i]['sp'])
        print (msg)
    data = {"data":r.json()['data']}
    set_schedule (cookie,4,data)



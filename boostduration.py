import requests
import json
import login
import zwaveapi

boostdur_url = login.api+"hillview/boostduration/"
boostrem_url = login.api+"hillview/boosttime/"

def get_boostTime (cookie,id):
    # request the boost time remaining
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    r = requests.get(boostrem_url+str(id),headers=headers)

    return r    

def get_boostDuration (cookie,id):
    # request the boost duration
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    r = requests.get(boostdur_url+str(id),headers=headers)

    return r

def set_boostDuration (cookie,id,payload):

    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now set the boost duration
    r = requests.post(boostdur_url+str(id),data=json.dumps(payload),headers=headers)

    return r

if __name__ == "__main__":

    print ("BoostDuration get/set test")
    roomid = int(input ("Enter id of room: "))
    
    cookie = login.send()
    s = get_boostDuration(cookie,roomid)
    print (s)
    boostDuration = s.json()['data']

    print (boostDuration)

    boostDuration = int(input("Enter new boost duration: "))
    payload = {'data':boostDuration}
    s = set_boostDuration(cookie,roomid,payload)
    print (s)

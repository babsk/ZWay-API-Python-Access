import requests
import json
import login
import zwaveapi

boostsp_url = login.api+"hillview/boostsp/"

def get_boostsp (cookie,id):
    # request the boost SP
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    r = requests.get(boostsp_url+str(id),headers=headers)

    return r

def set_boostsp (cookie,id,payload):

    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now set the boost SP
    r = requests.post(boostsp_url+str(id),data=json.dumps(payload),headers=headers)


if __name__ == "__main__":

    print ("BoostSP get/set test")
    roomid = int(input ("Enter id of room: "))
    
    cookie = login.send()
    s = get_boostsp(cookie,roomid)
    print (s)
    boostsp = s.json()['data']

    print (boostsp)

    boostsp = int(input("Enter new boost set point: "))
    payload = {'data':boostsp}
    s = set_boostsp(cookie,roomid,payload)
    print (s)

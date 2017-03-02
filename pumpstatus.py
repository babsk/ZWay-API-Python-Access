import requests
import json
import login
import zwaveapi

pumpstatus_url = login.api+"hillview/pumpstatus/"

def get_pumpstatus (cookie,id):
    # request the pump status
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    r = requests.get(pumpstatus_url+str(id),headers=headers)

    return r

def set_pumpstatus (cookie,id,payload):

    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now set the pump status
    r = requests.post(pumpstatus_url+str(id),data=json.dumps(payload),headers=headers)

    return r


if __name__ == "__main__":

    print ("Pump Status get/set test")
    roomid = 1
    
    cookie = login.send()
    s = get_pumpstatus(cookie,roomid)
    print (s)
    pumpstatus = s.json()['data']

    print (pumpstatus)

    pumpstatus = input("Enter new pump status (true or false): ")
    payload = {'data':pumpstatus}
    s = set_pumpstatus(cookie,roomid,payload)
    print (s)

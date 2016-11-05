import requests
import json
import login
import zwaveapi

mode_url = login.api+"hillview/mode/"

def get_mode (cookie,id):
    # request the mode
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    r = requests.get(mode_url+str(id),headers=headers)

    return r

def set_mode (cookie,id,payload):

    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now set the mode
    r = requests.post(mode_url+str(id),data=json.dumps(payload),headers=headers)


if __name__ == "__main__":

    print ("Mode get/set test")
    roomid = int(input ("Enter id of room: "))
    
    cookie = login.send()
    s = get_mode(cookie,roomid)
    print (s)
    mode = s.json()['data']

    print (mode)

    mode = int(input("Enter new mode: "))
    payload = {'data':mode}
    s = set_mode(cookie,roomid,payload)
    print (s)

#print ("device id        name          owner")
#for i in devices.keys():
#    msg = "" + str(i) + "     "+str(devices[i]['data']['givenName']['value'])+"           "
#    for j in range(len(roomData)):
#        if int(i) in roomData[j]['nodes']:
#            msg += str(j)
#    print (msg)
#

import requests
import json

api="http://192.168.1.180:8083/ZAutomation/api/v1/"
username='admin'
password='hillview'

login_url = api+"login"

def login ():
    # post a login request
    headers={'accept':'application/json','Content-Type':'application/json'}
    payload = {'form': 'True','login':'admin','password':'hillview','keepme':'false','default_ui':'1'}
    r = requests.post(login_url,data=json.dumps(payload),headers=headers)

    # extract the cookie from the response
    cookie = r.json()['data']['sid']
    return cookie

# send a request to get the data tree from the ZWaveAPI
def get_devices (cookie):

    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now get the data
    r = requests.get(api+'devices',data=json.dumps({}),headers=headers)
    return r

cook = login()

# now that we are logged in we need to use the cookie in future requests
r = get_devices (cook)

devices = r.json()['devices']

print ("device id        name          owner")
for i in devices.keys():
    msg = "" + str(i) + "     "+str(devices[i]['data']['givenName']['value'])+"           "
    for j in range(len(roomData)):
        if int(i) in roomData[j]['nodes']:
            msg += str(j)
    print (msg)

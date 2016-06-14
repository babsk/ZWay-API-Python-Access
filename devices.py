import requests
import json
import login
import zwaveapi
import rooms

cookie = login.send()
r = zwaveapi.get_zwaveapi_data (cookie)
devices = r.json()['devices']
s = rooms.get_rooms(cookie)
roomData = s.json()['data']

print ("device id        name          owner")
for i in devices.keys():
    msg = "" + str(i) + "     "+str(devices[i]['data']['givenName']['value'])+"           "
    for j in range(len(roomData)):
        if int(i) in roomData[j]['nodes']:
            msg += str(j)
    print (msg)

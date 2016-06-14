import requests
import json
import login
import zwaveapi
import rooms

cookie = login.send()
r = zwaveapi.get_zwaveapi_data (cookie)
devices = r.json()['devices']

for i in devices.keys():
    trv = devices[i]['data']['deviceTypeString']['value'] == 'Thermostat'
    if trv:
        print (devices[i]['data']['givenName']['value'] + ": " + str(devices[i]['instances']['0']['commandClasses']['67']['data']['1']['val']['value']))
#   msg = "" + str(i) + "     "+str(devices[i]['data']['givenName']['value'])+"           "


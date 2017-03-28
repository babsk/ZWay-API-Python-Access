##################################################################
#
# SWITCH.PY
#
# This script provides functions to get and set the status of
# binary power switches in the standard zway API
#
# It can be run standalone, in which case it logs in, requests a
# device id from the user, verifies it is a switch, gets the
# current status and sets the status to a value provided by the
# user
#
# NOTE: before making a call to get the data it is necessary to
#       send a login request and provide the resulting cookie
#       for subseqent API requests.
#
##################################################################
import requests
import json
import login
import zwaveapi

def get_device_type (cookie,id):
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now get the data
    r = requests.get(zwaveapi.api+"Run/zway.devices["+str(id)+"].data.deviceTypeString",data=json.dumps({}),headers=headers)
    device = r.json()['value']
    return device

def get_switch_status (cookie,id):
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now get the data
    r = requests.get(zwaveapi.api+"Run/zway.devices["+str(id)+"].commandClasses[37].data.level.value",data=json.dumps({}),headers=headers)
    status = r.json()
    return status

def set_switch_status (cookie,id,status):
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now get the data
    r = requests.get(zwaveapi.api+"Run/zway.devices["+str(id)+"].commandClasses[37].Set("+status+")",data=json.dumps({}),headers=headers)
    return r 

if __name__ == "__main__":

    print ("Switch get/set test")
    switchid = int(input ("Enter device id of switch: "))
    
    cookie = login.send()
    s = get_device_type(cookie,switchid)

    if (s == 'Binary Power Switch'):
        status = get_switch_status (cookie,switchid)
        print ("Status of switch " + str(switchid) + " is " + str(status))
        status = input("Enter new status of switch(true or false): ")
        r = set_switch_status(cookie,switchid,status)
        print (r)
    else:
        print ("Device " + str(switchid) + " is not a switch (" + s + ")")


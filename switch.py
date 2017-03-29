##################################################################
#
# SWITCH.PY
#
# This script provides functions to get and set the status of
# binary power switches in the standard zway automation API
#
# It can be run standalone, in which case it logs in, retrieves
# a list of switches and displays them, requests a device id from
# the user, and gets the
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

def get_binary_switches (cookie):
    switches = []
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now get the data
    r = requests.get(login.api+"devices",data=json.dumps({}),headers=headers)
    device_list = r.json()['data']['devices']
    for i in range (0,len(device_list)):
        if device_list[i]['deviceType'] == 'switchBinary':
            switches.insert(i,device_list[i])
    return switches

def get_switch_status (cookie,id):
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now get the data
    r = requests.get(login.api+"devices/"+id,data=json.dumps({}),headers=headers)
    status = r.json()['data']['metrics']['level']
    return status

def set_switch_status (cookie,id,status):
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now get the data
    r = requests.get(login.api+"devices/"+id+"/command/"+status,data=json.dumps({}),headers=headers)
    return r 

if __name__ == "__main__":

    cookie = login.send()
    s = get_binary_switches(cookie)
    for i in range (0,len(s)):
        msg = "" + str(s[i]['id'] + "      " + s[i]['metrics']['title'])
        print (msg)
    
    print ("Switch get/set test")
    switchid = input ("Enter device id of switch: ")

    status = get_switch_status (cookie,switchid)
    print ("Status of switch " + str(switchid) + " is " + str(status))
    status = input("Enter new status of switch(on or off): ")
    r = set_switch_status(cookie,switchid,status)
    print (r)



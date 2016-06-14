import requests
import json
import login

api = "http://"+login.myip+":8083/ZWaveAPI/"

zwaveapi_data = api + "Data/0"

# send a request to get the data tree from the ZWaveAPI
def get_zwaveapi_data (cookie):

    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    # now get the data
    r = requests.post(zwaveapi_data,data=json.dumps({}),headers=headers)
    return r
    
if __name__ == "__main__":
    cookie = login.send()
    r = get_zwaveapi_data (cookie)

    controller_id = r.json()['controller']['data']['nodeId']['value']
    print ("controller id is " + str(controller_id))
    devices = r.json()['devices']
    numDevices = len(r.json()['devices'])
    print ("number of physical devices is " + str(numDevices))
    for i in devices.keys():
        print (str(i)+": " + str(devices[i]['data']['vendorString']['value']))


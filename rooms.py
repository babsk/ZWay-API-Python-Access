import requests
import json
import login

rooms_url = login.api+"hillview/rooms"

def display_rooms (r):
    rooms_list = r.json()['data']
    print ("room id     name")
    for i in range (0,len(rooms_list)):
        msg = "" +str(rooms_list[i]['id']) + "           " + str(rooms_list[i]['title']);
        print (msg);

def add_room (cookie,name):
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    payload = {'name': name}
    print (payload)
    r = requests.post(rooms_url,data=json.dumps(payload),headers=headers)


def get_rooms (cookie):
    
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    r = requests.get(rooms_url,headers=headers)

    return r

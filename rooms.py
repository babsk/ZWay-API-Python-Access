import requests
import json
import login

rooms_url = login.api+"hillview/rooms"

def get_rooms (cookie):
    
    headers={'accept':'application/json','Content-Type':'application/json','Cookie':'ZWAYSession='+cookie}
    r = requests.get(rooms_url,headers=headers)

    return r

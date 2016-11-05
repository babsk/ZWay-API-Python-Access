import requests
import json

# ip address of my raspberry pi
myip="192.168.1.180"
api = "http://"+myip+":8083/ZAutomation/api/v1/"
login_url = api+"login"

def send ():
    # post a login request
    headers={'accept':'application/json','Content-Type':'application/json'}
    payload = {'form': 'True','login':'admin','password':'hillview','keepme':'false','default_ui':'1'}
    r = requests.post(login_url,data=json.dumps(payload),headers=headers)

    # extract the cookie from the response
    cookie = r.json()['data']['sid']
    return cookie

if __name__ == "__main__":
    print (send())


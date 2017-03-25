##################################################################
#
# LOGIN.PY
#
# This script sends a standard login request to the zway server.
#
# It can be run standalone, in which case it just prints out the
# cookie that is returned.
#
# When imported into other scripts a call to login.send() returns
# the cookie which must be stored and used for subsequent Zway API
# requests.
#
# NOTE: before using this script, make sure secrets.py has been
#       updated with your own raspberry pi / zway details
#
##################################################################

import requests
import json
import secrets

api = "http://"+secrets.myip+":8083/ZAutomation/api/v1/"
login_url = api+"login"

def send ():
    # post a login request
    headers={'accept':'application/json','Content-Type':'application/json'}
    payload = {'form': 'True','login':secrets.username,'password':secrets.password,'keepme':'false','default_ui':'1'}
    r = requests.post(login_url,data=json.dumps(payload),headers=headers)

    # extract the cookie from the response
    cookie = r.json()['data']['sid']
    return cookie

if __name__ == "__main__":
    print (send())


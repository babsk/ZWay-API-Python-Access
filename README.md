# ZWay-API-Python-Access
Python scripts for accessing the ZWave API of a raspberry pi running the ZWay home automation server from [ZWave.me](zwave.me).

Initially used as quick ways to test and for 'proof of concept' for custom additions to the automation API.
Now being extended and improved to provide access from a personal Amazon Alexa Smart Home Skill via a AWS Lambda function written in python.

Before running any of these scripts it is necessary to edit **secrets.py** to include an IP address (local or external) and the login credentials for the ZWave SmartHome server.

## Standard API scripts
The following scripts all work with the standard ZWave APIs:
* **http://(ip address):8083/ZWaveAPI** 
* **http://(ip address):8083/ZAutomation/api/v1**


file | comments
-----|----------
**secret.py**|edit this to provide IP address and SmartHome login credentials
**login.py**|function to send a login request and return the resulting cookie (required by all other requests)
**zwaveapi.py**|definition of the **ZWaveAPI** and a function to access the data tree
**trvs.py**|requests a list of devices and displays those with the type 'thermostat'
**switch.py**|functions to get and set the status of devices that support commandClass 37 (binary switch)

## Custom API scripts
The following scripts will not work with the standard ZWay server. They work with a custom addition to the Automation API accessible via:
* **http://(ip address):8083/ZAutomation/api/v1/hillview**

file | comments
-----|----------
**boostduration.py**|functions to get and set the boost duration of a room
**boostsp.py**|functions to get and set the boost temperature of a room
**devices.py**|requests a list of devices and rooms and displays which room owns which device
**mode.py**|functions to get and set the mode of a room
**pumpstatus.py**|functions to get and set the status of the hot water pump
**rooms.py**|functions to get and display a list of rooms
**schedule.py**|functions to get and set the whole schedule for a room
**test.py**|miscellaneous testing
**test_room_add.py**|experimental room adding code

## Further Information
I have been successfully running various parts of my central heating system from a custom ZWay module since 2015.
This is an ongoing project which I occasionally blog about at [Misadventures in Home Automation](http://kershawkids.blogspot.co.uk/)
These python scripts have been uploaded for my own personal use and are for the most part only relevant for use with my custom ZWay server module (not available via github as yet). They were never intended for public use, but the standard scripts may be of use to anyone starting out with ZWay and as an alternative to the **curl** scripts provided in the ZWay developer documentation.

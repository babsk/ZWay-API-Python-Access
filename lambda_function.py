##################################################################
#
# LAMBDA_FUNCTION.PY
#
# This is the AWS lambda function allowing an Alexa Smart Home
# Skill to control my ZWay powered heating / home automation
# project.
#
# It makes extensive use of my own additions to the ZWay API.
#
# Devices are automatically discovered.
#
# The devices are the rooms (central heating zones) and
# binary switches, both of which are requested from the ZWay
# server during device discovery.
#
# requests library must be provided in the package deployment as
# it is not part of AWS lambda function environment
#
##################################################################

import requests
import json
import secrets
import login
import pumpstatus
import rooms
import mode
import boostduration
import boostsp
import switch

boostMode = 3

# this is the main entry point and is passed smart home
# directives from the Alexa ZWay skill
def lambda_handler(event, context):
    access_token = event['payload']['accessToken']

    if event['header']['namespace'] == 'Alexa.ConnectedHome.Discovery':
        return handleDiscovery(context, event)

    elif event['header']['namespace'] == 'Alexa.ConnectedHome.Control':
        return handleControl(context, event)
        
    elif event['header']['namespace'] == 'Alexa.ConnectedHome.Query':
        return handleQuery(context, event)

# this handles Discover directives from Alexa
# it returns 'devices' that can be managed by the Smarthome Skill
# rooms - turn on/off directives result in boost feature, temp and percentage are used for boost parameters
# water pump - turn on/off directives only
def handleDiscovery(context, event):
    payload = ''
    header = {
        "namespace": "Alexa.ConnectedHome.Discovery",
        "name": "DiscoverAppliancesResponse",
        "payloadVersion": "2"
        }
    switchActions = ["turnOn","turnOff"]
    roomActions = ["turnOn","turnOff","setTargetTemperature","setPercentage","getTargetTemperature","getTemperatureReading"]
    binarySwitch = {
                            "applianceId":"",
                            "manufacturerName":"yourManufacturerName",
                            "modelName":"model 01",
                            "version":"your software version number here.",
                            "friendlyName":"",
                            "friendlyDescription":"",
                            "isReachable":True,
                            "actions":switchActions,
                            "additionalApplianceDetails":{}
                        }

    if event['header']['name'] == 'DiscoverAppliancesRequest':
        discoveredAppliances = [];
        
        # get the switches
        cookie = login.send()
        s = switch.get_binary_switches(cookie)
        for i in range (0,len(s)):
            appliance = binarySwitch.copy()
            appliance['applianceId'] = s[i]['id']
            appliance['friendlyName'] = s[i]['metrics']['title']
            appliance['friendlyDescription'] = s[i]['deviceType']
            appliance['additionalApplianceDetails'] = {'type':s[i]['deviceType']}
            discoveredAppliances.insert (len(discoveredAppliances),appliance)
                        
        # the rest of the appliances are rooms which we need to request

        room_list = rooms.get_rooms(cookie).json()['data']

        for i in range (0,len(room_list)):
            appliance = binarySwitch.copy()
            appliance['applianceId'] = room_list[i]['id']
            appliance['friendlyName'] = str(room_list[i]['title'])
            appliance['friendlyDescription'] = "boost heating"
            appliance['actions'] = roomActions
            discoveredAppliances.insert(len(discoveredAppliances),appliance)        
        
        payload = {"discoveredAppliances": discoveredAppliances}
        
    return { 'header': header, 'payload': payload }

# this handles Control directives from Alexa
# it determines which device to control from the id
# directives are handled as follows:
#
# TurnOnRequest / TurnOffRequest - boost on / boost off
# SetTargetTemperatureRequest - set boost SP
# SetPercentageRequest - TODO - use for boost time?
def handleControl(context, event):
    payload = ''
    header = ''
    device_id = event['payload']['appliance']['applianceId']
    message_id = event['header']['messageId']
    control_type = event['header']['name']
    additional_details = event['payload']['appliance']['additionalApplianceDetails']
    if "type" in additional_details:
        device_type = additional_details['type']
    else:
        device_type = ""
    headerTemplate = {
                "namespace":"Alexa.ConnectedHome.Control",
                "payloadVersion":"2",
                "messageId": message_id
            }

    # is it a switch request
    if device_type == 'switchBinary':
        if (control_type == 'TurnOnRequest') or (control_type == 'TurnOffRequest'):
            cookie = login.send()    
            if control_type == 'TurnOnRequest':
                switch.set_switch_status(cookie,device_id,"on")
                headerTemplate['name'] = "TurnOnConfirmation"
                
            if event['header']['name'] == 'TurnOffRequest':
                switch.set_switch_status(cookie,device_id,"off")
                headerTemplate['name'] = "TurnOffConfirmation"
            header = headerTemplate
            payload = { }

    # must be a room request, but which type
    elif control_type == 'TurnOnRequest':
        # set mode to boost
        cookie = login.send()
        mode.set_mode(cookie,int(device_id),{'data':boostMode})
        headerTemplate['name'] = "TurnOnConfirmation"
        header = headerTemplate
        payload = { }
        
    elif control_type == 'TurnOffRequest':
        # set mode to base mode (turn off boost)
        cookie = login.send()
        base = mode.get_basemode(cookie,int(device_id))
        mode.set_mode(cookie,int(device_id),{'data':base.json()['data']})
        headerTemplate['name'] = "TurnOffConfirmation"
        header = headerTemplate
        payload = { }

    elif control_type == 'SetTargetTemperatureRequest':
        # set boostSP to temp in directive and activate boost
        cookie = login.send()
        sp = event['payload']['targetTemperature']['value']
        boostsp.set_boostsp(cookie,int(device_id),{'data':int(sp)})
        mode.set_mode(cookie,int(device_id),{'data':boostMode})
        headerTemplate['name'] = "SetTargetTemperatureConfirmation"
        payload = {
                    "targetTemperature":{"value":int(sp)},
                    "temperatureMode":{"value":"AUTO"},
                    "previousState":{"targetTemperature":{"value":10},"mode":{"value":"AUTO"}}
                }
        header = headerTemplate
        
    elif control_type == 'SetPercentageRequest':
        # set boost duration to value in directive and activate boost
        cookie = login.send()
        percent = int(event['payload']['percentageState']['value'])
        minutes = percent * 60
        boostduration.set_boostDuration(cookie,int(device_id),{'data':int(minutes)})
        mode.set_mode(cookie,int(device_id),{'data':boostMode})
        headerTemplate['name'] = "SetPercentageConfirmation"
        payload = {}
        header = headerTemplate
        
    return { 'header': header, 'payload': payload }

# this handles Query directives from Alexa
# it determines which device to query from the id
# directives are handled as follows:
#
# GetTargetTemperatureRequest
# GetTemperatureReadingRequest  
def handleQuery(context, event):
    payload = ''
    header = ''
    device_id = event['payload']['appliance']['applianceId']
    message_id = event['header']['messageId']
    query_type = event['header']['name']

    headerTemplate = {
                "namespace":"Alexa.ConnectedHome.Query",
                "payloadVersion":"2",
                "messageId": message_id
            }

    # assuming this is a room request, but which type
    if query_type == 'GetTargetTemperatureRequest':
        # get set point 
        cookie = login.send()
        setPoint = 0.0
        room_list = rooms.get_rooms(cookie).json()['data']
        for i in range (0,len(room_list)):
            if room_list[i]['id'] == int(device_id):
                setPoint = room_list[i]['desiredTemp']
        
        headerTemplate['name'] = "GetTargetTemperatureResponse"

        payload = {
                    "targetTemperature":{"value":setPoint},
                    "temperatureMode":{"value":"CUSTOM"}}
        header = headerTemplate
        
    elif query_type == 'GetTemperatureReadingRequest':
        # get set point 
        cookie = login.send()
        currentTemp = 0.0
        room_list = rooms.get_rooms(cookie).json()['data']
        for i in range (0,len(room_list)):
            if room_list[i]['id'] == int(device_id):
                currentTemp = room_list[i]['currentTemp']
        
        headerTemplate['name'] = "GetTemperatureReadingResponse"

        payload = {
                    "temperatureReading":{"value":currentTemp}}
        header = headerTemplate

                                 

    return { 'header': header, 'payload': payload } 

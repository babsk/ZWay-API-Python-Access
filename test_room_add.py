import requests
import json
import rooms
import login 

cookie = login.send()

# first get rooms and display
r = rooms.get_rooms (cookie)
rooms.display_rooms (r)

roomName = str(input("Enter name of new room: "))
rooms.add_room(cookie,roomName)










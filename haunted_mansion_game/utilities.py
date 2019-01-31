"""
This file contains global functions that will be helpful
"""


def get_room_by_name(room_name, list_of_rooms):
    for room in list_of_rooms:
        if room_name == room.roomName:
            return room


def get_item_by_name(item_name, list_of_items):
    for item in list_of_items:
        if item_name == item.itemName:
            return item


def display_room_msg(room_name):
    if room_name.visited:
        print room_name.shortMSG
    else:
        print room_name.longMSG
    print "***ROOM FEATURE***"
    for feature in room_name.features:
        print feature
    return


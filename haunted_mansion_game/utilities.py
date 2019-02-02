"""
This file contains global functions that will be helpful
"""
from actions import *


def get_room_by_name(room_name, list_of_rooms):
    for room in list_of_rooms:
        if room_name.lower() == room.roomName.lower():
            return room


def get_item_by_name(item_name, list_of_items):
    for item in list_of_items:
        if item_name == item.itemName:
            return item


def execute_action(parsed_command, game_state):
    # TODO: Jeremy to handle missing keys
    method = getattr(Actions, parsed_command["verb"])
    if parsed_command["room"]:
        method(game_state, parsed_command["room"])
    elif parsed_command["feature"]:
        method(game_state, parsed_command["feature"])
    elif parsed_command["object"]:
        method(game_state, parsed_command["object"])

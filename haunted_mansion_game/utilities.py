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


def get_feature_by_name(feature_name, list_of_features):
    for feature in list_of_features:
        if feature_name == feature.name:
            return feature


def execute_action(parsed_command, game_state):
    if parsed_command["verb"] is "" or "verb" not in parsed_command:
        method = getattr(Actions, "go")
    else:
        method = getattr(Actions, parsed_command["verb"])
    method(game_state, parsed_command)

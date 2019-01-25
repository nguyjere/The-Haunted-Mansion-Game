import os
from room import *
from item import *
from player import *


# this function is currently broken
# room, item, and player __init__ can only access ../resources/
def load_game(saved_game):
    player = None
    list_of_rooms = []
    list_of_items = []
    player = Player("player.json")
    for file_name in os.listdir('../saved_games/{}/rooms/'.format(saved_game)):
        list_of_rooms.append(Room(file_name))
    for file_name in os.listdir('../saved_games/{}/items/'.format(saved_game)):
        list_of_items.append(Item(file_name))
    return player, list_of_rooms, list_of_items


def load_new_game():
    player = None
    list_of_rooms = []
    list_of_items = []
    player = Player("player.json")
    for file_name in os.listdir('../resources/rooms/'):
        list_of_rooms.append(Room(file_name))
    for file_name in os.listdir('../resources/items/'):
        list_of_items.append(Item(file_name))
    return player, list_of_rooms, list_of_items


def save_game(save_name, player, list_of_rooms, list_of_items):
    if not os.path.isdir('../saved_games/{}'.format(save_name)):
        os.mkdir('../saved_games/{}'.format(save_name))
    for folder in ["player", "rooms", "items"]:
        if not os.path.isdir('../saved_games/{}/{}'.format(save_name, folder)):
            os.mkdir('../saved_games/{}/{}'.format(save_name, folder))
    player.save_json("../saved_games/{}/player/player.json".format(save_name))
    for room in list_of_rooms:
        room.save_json("../saved_games/{}/rooms/{}.json".format(save_name, room))
    for item in list_of_items:
        item.save_json("../saved_games/{}/items/{}.json".format(save_name, item))
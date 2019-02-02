import os
from room import *
from item import *
from player import *
from utilities import *


class GameState:
    def __init__(self, saved_game=None):
        self.player = None
        self.rooms = None
        self.items = None
        if saved_game:
            self.load_game(saved_game)
        else:
            self.load_new_game()

    def load_game(self, saved_game):
        self.player = None
        self.rooms = []
        self.items = []
        self.player = Player("player.json")
        for file_name in os.listdir('../saved_games/{}/rooms/'.format(saved_game)):
            self.rooms.append(Room(file_name))
        for file_name in os.listdir('../saved_games/{}/items/'.format(saved_game)):
            self.items.append(Item(file_name))
        return self.player, self.rooms, self.items

    def load_new_game(self):
        self.player = None
        self.rooms = []
        self.items = []
        self.player = Player("player.json")
        for file_name in os.listdir('../resources/rooms/'):
            self.rooms.append(Room(file_name))
        for file_name in os.listdir('../resources/items/'):
            self.items.append(Item(file_name))
        return self.player, self.rooms, self.items

    def save_game(self, save_name):
        if not os.path.isdir('../saved_games/{}'.format(save_name)):
            os.mkdir('../saved_games/{}'.format(save_name))
        for folder in ["player", "rooms", "items"]:
            if not os.path.isdir('../saved_games/{}/{}'.format(save_name, folder)):
                os.mkdir('../saved_games/{}/{}'.format(save_name, folder))
        self.player.save_json("../saved_games/{}/player/player.json".format(save_name))
        for room in self.rooms:
            room.save_json("../saved_games/{}/rooms/{}.json".format(save_name, room))
        for item in self.items:
            item.save_json("../saved_games/{}/items/{}.json".format(save_name, item))

    def get_current_room(self):
        return get_room_by_name(self.player.currentRoom, self.rooms)

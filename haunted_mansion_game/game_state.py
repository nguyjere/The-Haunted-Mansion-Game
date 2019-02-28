import os
from room import *
from feature import *
from item import *
from player import *
from actions import *


class GameState:

    def __init__(self, saved_game=None):
        self.player = None
        self.rooms = None
        self.features = None
        self.items = None
        if saved_game:
            self.load_game(saved_game)
        else:
            self.load_new_game()

    def load_game(self, saved_game):
        self.player = None
        self.rooms = []
        self.features = []
        self.items = []
        self.player = Player("player.json", saved_game)
        for file_name in os.listdir('../saved_games/{}/rooms/'.format(saved_game)):
            self.rooms.append(Room(file_name))
        for file_name in os.listdir('../saved_games/{}/features/'.format(saved_game)):
            self.features.append(Features(file_name))
        for file_name in os.listdir('../saved_games/{}/items/'.format(saved_game)):
            self.items.append(Item(file_name))
        return self.player, self.rooms, self.features, self.items

    def load_new_game(self):
        self.player = None
        self.rooms = []
        self.features = []
        self.items = []
        self.player = Player("player.json")
        for file_name in os.listdir('../resources/rooms/'):
            self.rooms.append(Room(file_name))
        for file_name in os.listdir('../resources/features/'):
            self.features.append(Features(file_name))
        for file_name in os.listdir('../resources/items/'):
            self.items.append(Item(file_name))
        return self.player, self.rooms, self.features, self.items

    def save_game(self, save_name):
        if not os.path.isdir('../saved_games/{}'.format(save_name)):
            os.mkdir('../saved_games/{}'.format(save_name))
        for folder in ["player", "rooms", "features", "items"]:
            if not os.path.isdir('../saved_games/{}/{}'.format(save_name, folder)):
                os.mkdir('../saved_games/{}/{}'.format(save_name, folder))
        self.player.save_json("../saved_games/{}/player/player.json".format(save_name))
        for room in self.rooms:
            room.save_json("../saved_games/{}/rooms/{}.json".format(save_name, room))
        for feature in self.features:
            feature.save_json("../saved_games/{}/features/{}.json".format(save_name, feature))
        for item in self.items:
            item.save_json("../saved_games/{}/items/{}.json".format(save_name, item))

    def get_current_room(self):
        return self.get_room_by_name(self.player.currentRoom)

    # FIXME: Crashes when it tries to print displayName of features without json files
    def display_current_room(self):
        current_room = self.get_current_room()
        current_room.display_room_msg()
        print "***ROOM FEATURE***"
        for feature in current_room.features:
            print self.get_feature_by_name(feature).displayName
        print "***NEXT ROOMS***"
        for room in current_room.connectedTo:
            print self.get_room_by_name(room).displayName
        print "***ITEMS***"
        for item in current_room.objects:
            print self.get_item_by_name(item).displayName
        print ""

    def execute_action(self, parsed_command):
        if "verb" not in parsed_command or parsed_command["verb"] is "":
            method = getattr(Actions, "go")
        else:
            method = getattr(Actions, parsed_command["verb"])
        method(self, parsed_command)

    def get_room_by_name(self, room_name):
        for room in self.rooms:
            if room_name.lower() == room.roomName.lower():
                return room

    def get_item_by_name(self, item_name):
        for item in self.items :
            if item_name.lower() == item.name.lower():
                return item

    def get_feature_by_name(self, feature_name):
        for feature in self.features:
            if feature_name.lower() == feature.name.lower():
                return feature

    def poison_effect(self):
        # If player takes 12 steps while poisoned, the game ends
        if self.player.poisonedSteps == 3:
            print "You start having a coughing fit."
        elif self.player.poisonedSteps == 6:
            print "You puked bile on the floor."
        elif self.player.poisonedSteps == 9:
            print "Your mouth starts to foam with blood."
        elif self.player.poisonedSteps == 12:
            print "You collapse on the ground and seized. You died."
            exit()
        self.player.poisonedSteps += 1

    def cure_poison(self):
        if self.player.status == "poisoned":
            self.player.status = "Alive"
            print "You feel much better now."
        else:
            print "You feel no difference."


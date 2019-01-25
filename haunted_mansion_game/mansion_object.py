"""
This super class is inherited by other objects in the game

Create an object from a json file by passing the filename into init

Ex. x = MansionObject("../resources/player/player.json")
"""

import json


class MansionObject:

    def __init__(self, file_name):
        self.__dict__ = self.get_json(file_name)

    def get_json(self, file_name):
        with open(file_name, "r") as read_file:
            res = json.load(read_file)
        return res

    def save_json(self, file_name):
        with open(file_name, "w") as write_file:
            json.dump(self.__dict__, write_file)

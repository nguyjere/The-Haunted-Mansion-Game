"""
This class describes the player defined in ../resources/player/
"""

from mansion_object import MansionObject


class Player(MansionObject):

    # TODO: Modify this __init__ to take saved_game, like the example in room.py
    def __init__(self, player):
        player_file = "../resources/player/{}".format(player)
        MansionObject.__init__(self, player_file)

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        self.inventory.remove(item)

    def show_inventory(self):
        for item in self.inventory:
            print item




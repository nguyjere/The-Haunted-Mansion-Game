"""
This class describes the player defined in ../resources/player/
"""

from mansion_object import MansionObject


class Player(MansionObject):

    def __init__(self, player, saved_game=None):
        if saved_game:
            player_file = "../saved_games/{}/player/{}".format(saved_game, player)
        else:
            player_file = "../resources/player/{}".format(player)
        MansionObject.__init__(self, player_file)

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        self.inventory.remove(item)





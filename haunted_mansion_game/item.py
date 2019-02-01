"""
This class describes the items defined in ../resources/items/
"""

from mansion_object import MansionObject


class Item(MansionObject):

    def __init__(self, item_name, saved_game=None):
        if saved_game:
            item_file = "../saved_games/{}/items{}".format(saved_game, item_name)
        else:
            item_file = "../resources/items/{}".format(item_name)
        MansionObject.__init__(self, item_file)

    def __str__(self):
        return self.name
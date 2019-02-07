"""
This class describes the items defined in ../resources/features/
"""

from mansion_object import MansionObject


class Features(MansionObject):

    def __init__(self, item_name, saved_game=None):
        if saved_game:
            item_file = "../saved_games/{}/features{}".format(saved_game, item_name)
        else:
            item_file = "../resources/features/{}".format(item_name)
        MansionObject.__init__(self, item_file)

    def __str__(self):
        return self.name

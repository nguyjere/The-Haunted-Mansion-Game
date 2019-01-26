"""
This class describes the items defined in ../resources/items/
"""

from mansion_object import MansionObject


class Item(MansionObject):

    # TODO: Modify this __init__ to take saved_game, like the example in room.py
    def __init__(self, item_name):
        item_file = "../resources/items/{}".format(item_name)
        MansionObject.__init__(self, item_file)

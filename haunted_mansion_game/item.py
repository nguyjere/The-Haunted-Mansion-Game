"""
This class describes the items defined in ../resources/items/
"""

from mansion_object import MansionObject


class Item(MansionObject):

    def __init__(self, item_name):
        item_file = "../resources/items/{}.json".format(item_name)
        MansionObject.__init__(self, item_file)

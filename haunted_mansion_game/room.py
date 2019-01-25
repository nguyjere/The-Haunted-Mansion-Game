"""
This class describes the room defined in ../resources/rooms/
"""

from mansion_object import MansionObject


class Room(MansionObject):

    def __init__(self, room_name):
        room_file = "../resources/room/{}.json".format(room_name)
        MansionObject.__init__(self, room_file)

    def include_item(self, item):
        pass

    def remove_item(self, item):
        pass

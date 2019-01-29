"""
This class describes the room defined in ../resources/rooms/
"""

from mansion_object import MansionObject


class Room(MansionObject):

    # TODO: Fix this function to take saved_game to load from saved game folder
    def __init__(self, room_name, saved_game = None):
        if saved_game:
            room_file = "the path to the room folder in saved game"
        else:
            room_file = "../resources/rooms/{}".format(room_name)
        MansionObject.__init__(self, room_file)

    def __str__(self):
        return self.roomName

    def include_item(self, item):
        pass

    def remove_item(self, item):
        pass

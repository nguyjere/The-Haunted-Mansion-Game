"""
This class describes the room defined in ../resources/rooms/
"""

from mansion_object import MansionObject


class Room(MansionObject):

    def __init__(self, room_name, saved_game=None):
        if saved_game:
            room_file = "../saved_games/{}/rooms/{}".format(saved_game, room_name)
        else:
            room_file = "../resources/rooms/{}".format(room_name)
        MansionObject.__init__(self, room_file)

    def __str__(self):
        return self.roomName

    def display_room_msg(self):
        if self.visited:
            print self.shortMSG
        else:
            print self.longMSG

    def include_item(self, item):
        self.objects.append(item)

    def remove_item(self, item):
        self.objects.remove(item)

    #used to "kill" the zombie
    def remove_feature(self, feature):
        self.features.remove(feature)

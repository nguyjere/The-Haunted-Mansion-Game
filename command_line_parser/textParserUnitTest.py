import unittest
from haunted_mansion_game.room import *
from textParser import *

textParser = TextParser()


class TestTextParser(unittest.TestCase):

    def test_go_north(self):
        test_room_obj = Room("barLounge.json")
        command = "go north"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'direction': 'north', 'verb': 'go', 'room': ''}

    def test_go_living_room(self):
        test_room_obj = Room("barLounge.json")
        command = "go to living room"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'direction': '', 'verb': 'go', 'room': 'livingroom'}

    def test_look_pool_table(self):
        test_room_obj = Room("barLounge.json")
        command = "look at pool table"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'preposition': 'at', 'verb': 'look', 'feature': u'pooltable'}

    # def test_open_french_door(self):
    #     test_room_obj = Room("barLounge.json")
    #     command = "open the french door"
    #     parsedCommand = textParser.getCommand(command, test_room_obj)
    #     assert parsedCommand == {'preposition': '', 'verb': 'open', 'feature': u'frenchdoor'}
    #     print parsedCommand

    def test_take_wine_bottle(self):
        test_room_obj = Room("barLounge.json")
        command = "take the wine bottle"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'verb': 'take', 'object': u'winebottle'}

    def test_look_without_at(self):
        test_room_obj = Room("barLounge.json")
        command = "look"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'preposition':'', 'verb': 'look', 'feature':''}

    def test_meta_command(self):
        test_room_obj = Room("barLounge.json")
        command = "inventory"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'verb': 'inventory'}
        command = "help"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'verb': 'help'}
        command = "savegame"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'verb': 'savegame'}
        command = "load game"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {'verb': 'loadgame'}

    def test_duplicate_keyword_prevention(self):
        test_room_obj = Room("barLounge.json")
        command = "go take winebottle"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {}

        command = "take winebottle look"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {}

        command = "take winebottle look help"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {}

        # to run this, temporarily add pear to barLounge
        #command = "take winebottle pear"
        #parsedCommand = textParser.getCommand(command, test_room_obj)
        #assert parsedCommand == {}

        #To do: prevent this
        #command = "go north take winebottle"
        #parsedCommand = textParser.getCommand(command, test_room_obj)
        #assert parsedCommand == {}

    def test_room_and_direction_prevention(self):
        test_room_obj = Room("barLounge.json")
        command = "go north living room"
        parsedCommand = textParser.getCommand(command, test_room_obj)
        assert parsedCommand == {}

if __name__ == '__main__':
    unittest.main()
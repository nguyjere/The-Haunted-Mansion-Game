import unittest
from haunted_mansion_game.room import *
from haunted_mansion_game.player import *
from textParser import *

textParser = TextParser()


class TestTextParser(unittest.TestCase):



    def test_go_living_room(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "go to living room"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'direction': '', 'verb': 'go', 'room': 'livingroom'}

    def test_look_pool_table(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "look at pool table"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'preposition': 'at', 'verb': 'look', 'feature': u'pooltable', 'object': ''}

    def test_look_wine_bottle(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "look at wine bottle"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'preposition': 'at', 'verb': 'look', 'feature': '', 'object': u'winebottle'}

    def test_look_inventory_object(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "look at doll"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'preposition': 'at', 'verb': 'look', 'feature': '', 'object': u'doll'}





    def test_take_wine_bottle(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "take the wine bottle"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'take', 'object': u'winebottle'}

    def test_look_without_at(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "look"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'preposition':'', 'verb': 'look', 'feature':'', 'object': ''}

    def test_meta_command(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "inventory"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'inventory'}
        command = "help"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'help'}
        command = "savegame"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'savegame'}
        command = "load game"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'loadgame'}

    def test_duplicate_keyword_prevention(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "go take winebottle"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        command = "take winebottle look"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        command = "take winebottle look help"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
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
        test_player_obj = Player("player.json")
        command = "go north living room"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

    def test_our_commands(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "consume wine bottle"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'consume', 'object': 'winebottle', 'feature': ''}

        command = "wine bottle consume"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        command = "consume"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        command = "hit pooltable"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'hit', 'feature': 'pooltable', 'object': ''}

        #you can only do one thing at a time
        command = "consume wine bottle hit pool table"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        command = "consume winebottle pooltable"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        #eventually, this should fail because it doesnt make sense. just testing turn on for now
        command = "turn on cabinet"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'turnon', 'feature': 'cabinet', 'object': ''}

    def test_command_on_object_in_inventory(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")
        command = "drop doll"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'drop', 'feature': '', 'object': 'doll'}
        command = "doll drop"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

    def test_command_is_compatible_with_object(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")

        command = "drop doll"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'drop', 'feature': '', 'object': 'doll'}

        command = "consume doll"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        command = "hit doll"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'hit', 'feature': '', 'object': 'doll'}

        command = "consume wine bottle"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'consume', 'feature': '', 'object': 'winebottle'}

        command = "turn off doll"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        command = "open recipe Book"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'open', 'feature': '', 'object': 'recipebook'}

    def test_synonym_replacement(self):
        test_room_obj = Room("barLounge.json")
        test_player_obj = Player("player.json")

        command = "lose doll"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'drop', 'feature': '', 'object': 'doll'}

        command = "eat wine bottle"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'consume', 'feature': '', 'object': 'winebottle'}

        command = "shut recipe book"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'close', 'feature': '', 'object': 'recipebook'}

    def test_direction_translation(self):
        test_room_obj = Room("hallway2.json")
        test_player_obj = Player("player.json")

        command = "down"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': '', 'room': 'hallway1', 'direction': ''}

        command = "go down"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'go', 'room': 'hallway1', 'direction': ''}

        command = "go southwest"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'go', 'room': 'guestRoom', 'direction': ''}

        command = "southwest"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': '', 'room': 'guestRoom', 'direction': ''}

        command = "go south west"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'go', 'room': 'guestRoom', 'direction': ''}

    def test_direction_translation_invalid(self):
        test_room_obj = Room("hallway2.json")
        test_player_obj = Player("player.json")
        command = "go north"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

        command = "north"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {}

    def test_drive_car(self):
        test_room_obj = Room("garage.json")
        test_player_obj = Player("player.json")
        command = "drive car"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'drive', 'feature': 'car', 'object': ''}

    def test_nonstandard_two_word_rooms(self):
        test_room_obj = Room("livingRoom.json")
        test_player_obj = Player("player.json")
        command = "go bar lounge"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'go', 'room': 'barlounge', 'direction': ''}


        command = "hallway 1"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': '', 'room': 'hallway1', 'direction': ''}

        command = "hallway1"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': '', 'room': 'hallway1', 'direction': ''}

        test_room_obj = Room("guestRoom.json")
        command = "go hallway 2"
        parsedCommand = textParser.getCommand(command, test_room_obj, test_player_obj)
        assert parsedCommand == {'verb': 'go', 'room': 'hallway2', 'direction': ''}

if __name__ == '__main__':
    unittest.main()
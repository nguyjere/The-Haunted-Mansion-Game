import unittest

from game import *

text_parser = TextParser()


class TestGame(unittest.TestCase):

    def test_load_game(self):
        game_state = GameState()
        assert game_state is not None

    def test_look_at_all_features(self):
        game_state = GameState()
        for room in game_state.rooms:
            game_state.player.currentRoom = room.__str__()
            for feature in room.features:
                feature_obj = game_state.get_feature_by_name(feature)
                user_input = "look at {}".format(feature_obj.displayName)
                parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
                if feature_obj.displayName not in ["bookshelf"]:
                    assert parsed_command
                    game_state.execute_action(parsed_command)

    def test_open_all_features(self):
        game_state = GameState()
        for room in game_state.rooms:
            game_state.player.currentRoom = room.__str__()
            for feature in room.features:
                feature_obj = game_state.get_feature_by_name(feature)
                user_input = "open {}".format(feature_obj.displayName)
                parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
                assert parsed_command
                if feature_obj.displayName not in ["doll house", "gun safe", "metal cabinet"]:
                    game_state.execute_action(parsed_command)

    def test_take_and_drop_all_items(self):
        game_state = GameState()
        current_room = game_state.get_current_room()
        for item in game_state.items:
            current_room.include_item(item.name)
        for item in game_state.items:
            item_obj = game_state.get_item_by_name(item.name)
            user_input = "take {}".format(item_obj.displayName)
            parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
            game_state.execute_action(parsed_command)
            assert item.name in game_state.player.inventory
            assert item.name not in current_room.objects
        for item in game_state.items:
            item_obj = game_state.get_item_by_name(item.name)
            user_input = "drop {}".format(item_obj.displayName)
            parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
            game_state.execute_action(parsed_command)
            assert item.name in current_room.objects
            assert item.name not in game_state.player.inventory

    def test_go_dining_room(self):
        game_state = GameState()

        user_input = "go to dining room"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)

        assert game_state.player.previousRoom == "livingRoom"
        assert game_state.player.currentRoom == "diningRoom"

    def test_pick_up_carkey(self):
        game_state = GameState()
        game_state.get_current_room().include_item("carKey")
        user_input = "take carkey"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)

        assert "carKey" in game_state.player.inventory

    def test_pick_up_car_key(self):
        game_state = GameState()
        game_state.get_current_room().include_item("carKey")
        user_input = "take car key"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)

        assert "carKey" in game_state.player.inventory

    def test_drop_car_key(self):
        game_state = GameState()
        game_state.get_current_room().include_item("carKey")
        user_input = "take car key"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)

        user_input = "drop car key"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)

        assert "carKey" not in game_state.player.inventory
        assert "carKey" in game_state.get_current_room().objects

    def test_look_at_features(self):
        game_state = GameState()

        user_input = "look at the sofa"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)

        user_input = "look at the console table"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)

    def test_look_at_objects(self):
        game_state = GameState()
        game_state.get_current_room().include_item("carKey")
        user_input = "look at the car key"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)

    def test_look_at_inventory_objects(self):
        game_state = GameState()
        game_state.get_current_room().include_item("carKey")
        user_input = "take the car key"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)
        # "look the car key" should be invalid. it should be "look at the car key"
        user_input = "look at the car key"
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        assert parsed_command
        game_state.execute_action(parsed_command)
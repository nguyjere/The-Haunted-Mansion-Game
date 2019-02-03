import utilities as util


class Actions:

    def __init__(self):
        pass

    @classmethod
    def go(cls, game_state, parsed_command):
        new_room_name = parsed_command["room"]
        # Update current room to visited
        current_room = game_state.get_current_room()
        current_room.visited = True
        # Update player's previous room to current room
        game_state.player.previousRoom = game_state.player.currentRoom
        # Update player's current room to the new room
        game_state.player.currentRoom = new_room_name
        # Display new room description
        new_room = game_state.get_current_room()
        new_room.display_room_msg()

    @classmethod
    def inventory(cls, game_state):
        game_state.player.show_inventory()

    @classmethod
    def help(cls, game_state):
        # TODO: Display list of available verbs
        pass

    @classmethod
    def savegame(cls, game_state):
        # TODO: Check if play.saveName is not None and Saved, else prompt for save name
        pass

    @classmethod
    def look(cls, game_state, parsed_command):
        if "feature" in parsed_command and parsed_command["feature"]:
            feature = util.get_feature_by_name(parsed_command["feature"], game_state.features)
            print feature.description
        # TODO: Need to parse for item before implementing "look at item"

    @classmethod
    def take(cls, game_state, parsed_command):
        # TODO: Need command parser to parse items before implementing
        pass
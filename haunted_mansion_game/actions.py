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
    def inventory(cls, game_state, *parsed_command):
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
        if "object" in parsed_command and parsed_command["object"] is not "":
            item_name = parsed_command["object"]
            item = util.get_item_by_name(item_name, game_state.items)
            game_state.player.add_to_inventory(item.name)
            game_state.get_current_room().remove_item(item.name)
            print "{} is added to your inventory.".format(item.name)
        else:
            print "You cannot take that."

    @classmethod
    def drop(cls, game_state, parsed_command):
        if "object" in parsed_command and parsed_command["object"] is not "":
            item_name = parsed_command["object"]
            item = util.get_item_by_name(item_name, game_state.items)
            game_state.player.remove_from_inventory(item.name)
            game_state.get_current_room().include_item(item.name)
            print "{} is dropped from your inventory.".format(item.name)
        else:
            print "You cannot drop that."

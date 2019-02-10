import haunted_mansion_game.game_state


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
        new_room = game_state.get_room_by_name(new_room_name)
        game_state.player.currentRoom = new_room.roomName
        # Display new room description
        game_state.display_current_room()

    @classmethod
    def inventory(cls, game_state, *parsed_command):
        for item in game_state.player.inventory:
            item_obj = game_state.get_item_by_name(item)
            item_name = item_obj.displayName
            item_desc = item_obj.description
            print "{} - {}".format(item_name, item_desc)

    @classmethod
    def help(cls, game_state):
        # TODO: Display list of available verbs
        pass

    @classmethod
    def savegame(cls, game_state, parsed_command):
        # Check if play.saveName is not None and Saved, else prompt for save name
        if game_state.player.saveName is None:
            print "Enter a game record name"
            game_file_name = raw_input(">>")
            game_state.player.saveName = game_file_name
            game_state.save_game(game_file_name)
        else:
            game_state.save_game(game_state.player.saveName)
            print "saved game state on : " + game_state.player.saveName
        pass

    @classmethod
    def look(cls, game_state, parsed_command):
        if "feature" in parsed_command and parsed_command["feature"]:
            feature = game_state.get_feature_by_name(parsed_command["feature"])
            print feature.description
        # FIXME: getCommand() for "look at <object>" does not return "object" key
        elif "object" in parsed_command and parsed_command["object"]:
            item = game_state.get_item_by_name(parsed_command["object"])
            print item.description

    @classmethod
    def take(cls, game_state, parsed_command):
        if "object" in parsed_command and parsed_command["object"] is not "":
            item_name = parsed_command["object"]
            item = game_state.get_item_by_name(item_name)
            game_state.player.add_to_inventory(item.name)
            game_state.get_current_room().remove_item(item.name)
            print "{} is added to your inventory.".format(item.name)
        else:
            print "You cannot take that."

    @classmethod
    def drop(cls, game_state, parsed_command):
        if "object" in parsed_command and parsed_command["object"] is not "":
            item_name = parsed_command["object"]
            item = game_state.get_item_by_name(item_name)
            game_state.player.remove_from_inventory(item.name)
            game_state.get_current_room().include_item(item.name)
            print "{} is dropped from your inventory.".format(item.name)
        else:
            print "You cannot drop that."

    @classmethod
    def lift(cls, game_state, parsed_command):
        # Check if feature or object then do something
        pass

    @classmethod
    def push(cls, game_state, parsed_command):
        pass

    @classmethod
    def consume(cls, game_state, parsed_command):
        pass

    @classmethod
    def open(cls, game_state, parsed_command):
        pass

    @classmethod
    def close(cls, game_state, parsed_command):
        pass

    @classmethod
    def turnon(cls, game_state, parsed_command):
        if "feature" in parsed_command:
            if parsed_command["feature"] is "TV":
                cls.turnon_tv(game_state)
            elif parsed_command["feature"] is "washingMachine":
                pass
            else:
                print "You can turn that on."
        elif "object" in parsed_command:
            pass
        else:
            print "Turn on what?"

    @classmethod
    def turnoff(cls, game_state, parsed_command):
        pass

    @classmethod
    def hit(cls, game_state, parsed_command):
        pass

    # This is an example. I don't think we actually have a TV
    @classmethod
    def turnon_tv(cls, game_state):
        TV = game_state.get_feature_by_name("TV")
        if TV.status == "off":
            TV.status = "on"
            # Maybe change the description as well, so the "look" message change
            print "You turned on the TV with CNN and the \"Great Wall of America\"."
        else:
            print "The TV is already turned on."

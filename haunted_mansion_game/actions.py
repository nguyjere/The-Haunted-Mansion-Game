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
        if game_state.player.status == "poisoned":
            game_state.poison_effect()

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
        elif "object" in parsed_command and parsed_command["object"]:
            item = game_state.get_item_by_name(parsed_command["object"])
            print item.description
        elif parsed_command["object"] == "" and parsed_command["feature"] == ""\
                and parsed_command["preposition"] == "":
            print game_state.display_current_room()

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
        if "object" in parsed_command:
            # FIXME: parsedCommand should give wineBottle instead of winebottle
            if parsed_command["object"] == "winebottle":
                cls.drink_wine(game_state)
            elif parsed_command["object"] == "antidote":
                cls.drink_antidote(game_state)
            else:
                print "You cannot consume that."
        else:
            print "Consume what?"


    @classmethod
    def open(cls, game_state, parsed_command):
        pass

    @classmethod
    def close(cls, game_state, parsed_command):
        pass

    @classmethod
    def turnon(cls, game_state, parsed_command):
        if "feature" in parsed_command:
            if parsed_command["feature"] == "car":
                cls.start_car(game_state)
            elif parsed_command["feature"] == "washingMachine":
                pass
            else:
                print "You can't turn that on."
        elif "object" in parsed_command:
            pass
        else:
            print "Turn on what?"

    @classmethod
    def turnoff(cls, game_state, parsed_command):
        if "feature" in parsed_command:
            if parsed_command["feature"] == "car":
                cls.turn_off_car(game_state)
            elif parsed_command["feature"] == "washingMachine":
                pass
            else:
                print "You can't turn that off."
        elif "object" in parsed_command:
            pass
        else:
            print "Turn off what?"

    @classmethod
    def hit(cls, game_state, parsed_command):
        # getting the car key from the zombie
        cls.hit_zombie(game_state, parsed_command)

    @classmethod
    def start_car(cls, game_state):
        car = game_state.get_feature_by_name("car")
        if car.running is False:
            if "carKey" in game_state.player.inventory and car.jumped is True:
                car.running = True
                game_state.player.remove_from_inventory("carKey")
                print "You turn the key in the ignition, and the car is now running."
            elif "carKey" in game_state.player.inventory and "carBatteryJumper" in game_state.player.inventory:
                car.running = True
                car.jumped = True
                game_state.player.remove_from_inventory("carKey")
                car.description = "A 90's Porsche 911. It's currently running."
                print "You open the door and pop the hood then attach battery jumper to the battery terminals " \
                      "in the car. Upon turning the keys the dash lights up and the car starts. " \
                      "The car is now running and you remove the batter jumper."
            elif "carKey" in game_state.player.inventory and car.jumped is False:
                car.description = "A 90's Porsche 911. Too bad the battery is dead."
                print "You open the door and attempt to start the car, but the car does not start, nor does the dash" \
                      "light up. The battery is probably dead."
            else:  # Case where the play does not have the car key
                print "The car is locked. You can't open the car without the car key."
        else:  # Case where the car is already running
            print "The car is already running."

    @classmethod
    def turn_off_car(cls, game_state):
        car = game_state.get_feature_by_name("car")
        if car.running is True:
            game_state.player.add_to_inventory("carKey")
            car.running = False
            car.description = "A 90's Porsche 911. It's currently turned off, but it starts perfectly now."
            print "You turned off the car and pocket the car key."
        else:
            print "The car is already turned off."

    @classmethod
    def drink_wine(cls, game_state):
        item_name = "wineBottle"
        game_state.player.status = "poisoned"
        wine_bottle = game_state.get_item_by_name(item_name)
        game_state.player.remove_from_inventory(wine_bottle.name)
        print "You drink from the wine bottle, then a few minutes later you start to feel sick."

    @classmethod
    def hit_zombie(cls, game_state, parsed_command):
        # getting the car key from the zombie
        if parsed_command["feature"] == "zombiesteward" and parsed_command["verb"] == "hit" \
                and "knife" in game_state.player.inventory:
            game_state.player.add_to_inventory("masterKey")
            game_state.get_current_room().remove_feature("zombieSteward")
            print "You killed the zombie. You found a master key among his remains!"
        if parsed_command["feature"] == "zombiesteward" and parsed_command["verb"] == "hit" \
                and "knife" not in game_state.player.inventory:
            print "You need a knife to do damage."

    @classmethod
    def drink_antidote(cls, game_state):
        item_name = "antidote"
        game_state.cure_poison()
        game_state.player.remove_from_inventory(item_name)

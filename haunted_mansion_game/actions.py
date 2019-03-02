import haunted_mansion_game.game_state


class Actions:

    def __init__(self):
        pass

    @classmethod
    def go(cls, game_state, parsed_command):
        new_room_name = parsed_command["room"]
        new_room = game_state.get_room_by_name(new_room_name)
        if new_room.locked is False:
            current_room = game_state.get_current_room()
            current_room.visited = True
            game_state.player.previousRoom = game_state.player.currentRoom
            game_state.player.currentRoom = new_room.roomName
            game_state.display_current_room()
            if game_state.player.status == "poisoned":
                game_state.poison_effect()
        else:
            print "This room is locked."

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
            if feature.name == "bookshelf":
                cls.pick_out_a_book(game_state)
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
            print "{} is dropped from your inventory.".format(item.displayName)
        else:
            print "You cannot drop that."

    @classmethod
    def lift(cls, game_state, parsed_command):
        # Check if feature or object then do something
        if "feature" in parsed_command:
            if parsed_command["feature"] == "bench":
                if game_state.player.status == "poisoned":
                    cls.lift_bench(game_state)
                else:
                    print "You're not strong enough to lift that."
            else:
                print "You can't lift that."
        else:
            print "Lift what?"
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
        if "feature" in parsed_command:
            if parsed_command["feature"] == "maingate": # FIXME: parsed_command should be mainGate instead?
                cls.cut_main_gate_lock(game_state)
            elif parsed_command["feature"] == "piano":
                cls.open_piano(game_state)
            elif parsed_command["feature"] == "dresser":
                cls.open_dresser(game_state)
            elif parsed_command["feature"] == "chest":
                cls.open_chest(game_state)
            elif parsed_command["feature"] == "pantry":
                cls.open_pantry(game_state)
            elif parsed_command["feature"] == "medicinecabinet":
                cls.open_medicineCabinet(game_state)
            elif parsed_command["feature"] == "filecabinet":
                cls.open_fileCabinet(game_state)
            else:
                print "You can't open that."
        else:
            print "Open what?"

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
    def drive(cls, game_state, parsed_command):
        if "feature" in parsed_command:
            if parsed_command["feature"] == "car":
                cls.drive_car(game_state)
            else:
                print "You can't drive that."
        else:
            print "Drive what?"

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
        print "You drink from the wine bottle. Suddenly you feel much stronger and lift heavier things."

    @classmethod
    def hit_zombie(cls, game_state, parsed_command):
        # getting the car key from the zombie
        if parsed_command["feature"] == "zombiesteward" and parsed_command["verb"] == "hit" \
                and "knife" in game_state.player.inventory:
            # note that the master key is not "in" the room, so we don't need to remove it from the room when the user picks it up
            game_state.player.add_to_inventory("masterKey")
            game_state.get_current_room().remove_feature("zombieSteward")
            print "You killed the zombie. You found a master key among his remains!"
        if parsed_command["feature"] == "zombiesteward" and parsed_command["verb"] == "hit" \
                and "knife" not in game_state.player.inventory:
            print "You need a knife to do damage."

    @classmethod
    def cut_main_gate_lock(cls, game_state):
        main_gate = game_state.get_feature_by_name("mainGate")
        if main_gate.locked is True:
            if "boltCutter" in game_state.player.inventory:
                main_gate.locked = False
                main_gate.description = "The gate is wide open to the darkness beyond. You probably don't want " \
                                        "to go out there; there might be killers and wolfs."
                print "Using the bolt cutter, you cut the chains off the gate and push the gate open to the endless " \
                      "path to darkness with creatures. Not a good idea to walk out."
            else:
                print "You cannot open the gate. It is locked with a chain and padlock."
        else:
            print "The main gate is already wide open"

    @classmethod
    def drive_car(cls, game_state):
        car = game_state.get_feature_by_name("car")
        current_room = game_state.get_current_room()
        main_gate = game_state.get_feature_by_name("mainGate")
        if car.running is True:
            if current_room.roomName == "garage":
                if main_gate.locked is False:
                    print "You drive the car out of the garage and through the gates, leaving this wrench house behind."
                    print "Congratulations, you've made it out alive! THE END."
                    exit()
                else:
                    print "You drive the car out of the garage into the courtyard. Unfortunately, the gate is locked "\
                          "and you probably don't want to wreck the only vehicle into the hardened gates. You stepped "\
                          "out of the car and out into the courtyard."
                    # Move car to courtyard
                    courtyard = game_state.get_room_by_name("courtyard")
                    current_room.features.remove("car")
                    courtyard.features.append("car")
                    # Move player to courtyard
                    current_room.visited = True
                    game_state.player.previousRoom = game_state.player.currentRoom
                    game_state.player.currentRoom = courtyard.roomName
            elif current_room.roomName == "courtyard":
                if main_gate.locked is False:
                    print "You drive the car through the gates, leaving this wrench house behind." \
                          "Congratulations, you've made it out alive! THE END."
                    exit()
                else:
                    print "The gate is still locked."
            else:
                # Logically this should never happen
                pass
        else:
            print "You cannot drive the car; it is not running. Start the car first."
            
    @classmethod
    def drink_antidote(cls, game_state):
        item_name = "antidote"
        game_state.cure_poison()
        game_state.player.remove_from_inventory(item_name)

    @classmethod
    def open_piano(cls, game_state):
        # note that the boltCutter is not "in" the room, so we don't need to remove it from the room when the user picks it up
        game_state.player.add_to_inventory("boltCutter")
        print "You found a boltcutter inside the piano. Might be useful."

    @classmethod
    def open_dresser(cls, game_state):
        # note that the carKey is not "in" the room, so we don't need to remove it from the room when the user picks it up
        game_state.player.add_to_inventory("carKey")
        print "You found a car key inside the dresser! Looks like it's for a Porsche!"

    @classmethod
    def open_chest(cls, game_state):
        print "The chest contains an old piece of paper. It says that your family name is: Imai. This sounds so familiar."

    @classmethod
    def open_pantry(cls, game_state):
        game_state.player.add_to_inventory("recipeBook")
        print "You found a recipe book, titled ALL NATURAL."
        print "It does seem to have cooking recipes but herbal mixing formulas."

    @classmethod
    def open_medicineCabinet(cls, game_state):
        game_state.player.add_to_inventory("antidote")
        print "You found an antidote. It says it clears an intoxicated condition.\nBut...it is up to you if you trust it or not."

    @classmethod
    def open_fileCabinet(cls, game_state):
        fileCabinet = game_state.get_feature_by_name("fileCabinet")
        if fileCabinet.object:
            game_state.player.add_to_inventory(fileCabinet.object)
            fileCabinet.object = None
            print "You found a family heirloom of a lion!"
        else:
            print "There is not thing interesting in this file cabinet."

    @classmethod
    def lift_bench(cls, game_state):
        game_state.player.add_to_inventory("carBatteryJumper")
        print "You found a car battery jumper!"

    @classmethod
    def unlock_secret_room(cls, game_state):
        library = game_state.get_room_by_name("library")
        secret_room = game_state.get_room_by_name("secretRoom")
        secret_room.locked = False
        secret_room.hidden = False
        library.connectedTo.append("secretRoom")
        library.longMSG += " You can access the secret room through the sliding door.\n"
        library.shortMSG += " east - sliding door to a secret room - 1st floor\n"
        library.roomEntry["sliding door"] = "secretRoom"
        library.directions["east"] = "secretRoom"
        print "As you attempt to pull the book out, you hear a loud click.\n" \
              "The book shelve slides open revealing another room!"

    @classmethod
    def pick_out_a_book(cls, game_state):
        print "Search an animal you want to read about. You might discover something new! (press enter to leave)"
        secret_room = game_state.get_room_by_name("secretRoom")
        while True:
            search_for = raw_input("Animal: ")
            if search_for == "":
                break
            elif search_for.lower() in ["lions", "lion"]:
                if secret_room.hidden:
                    cls.unlock_secret_room(game_state)
                    break
                else:
                    print "You already tried to pull that out. It's not actually a book, its a lever."
            elif search_for.lower() in ["dog", "dogs"]:
                print "You found a encyclopedia about dogs and now you're able to identify different breeds."
            # TODO: Add more animal entries
            else:
                print "That book is not found here."

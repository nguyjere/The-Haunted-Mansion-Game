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
            if game_state.player.bleeding:
                game_state.bleeding_effect()
        else:
            if "masterKey" in game_state.player.inventory:
                print "You unlocked this room using the master key."
                new_room.locked = False
                current_room = game_state.get_current_room()
                current_room.visited = True
                game_state.player.previousRoom = game_state.player.currentRoom
                game_state.player.currentRoom = new_room.roomName
                game_state.display_current_room()
                if game_state.player.status == "poisoned":
                    game_state.poison_effect()
                if game_state.player.bleeding:
                    game_state.bleeding_effect()
            else:
                print "This room is locked."

    @classmethod
    def back(cls, game_state, parsed_command):
        new_room_name = game_state.player.previousRoom
        # Update current room to visited
        current_room = game_state.get_current_room()
        current_room.visited = True
        # Update player's previous room to current room
        game_state.player.previousRoom = game_state.player.currentRoom
        # Update player's current room to the new room
        new_room = game_state.get_room_by_name(new_room_name)
        if new_room:
            game_state.player.currentRoom = new_room.roomName
            # Display new room description
            game_state.display_current_room()
            if game_state.player.status == "poisoned":
                game_state.poison_effect()
            if game_state.player.bleeding:
                game_state.bleeding_effect()

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
            if feature.name == "labTable":
                cls.make_life_potion(game_state)
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
                cls.open_file_cabinet(game_state)
            elif parsed_command["feature"] == "gunsafe":
                cls.open_gun_safe(game_state)
            elif parsed_command["feature"] == "metalcabinet":
                cls.open_metal_cabinet(game_state)
            else:
                if parsed_command["object"] == "picturebook":
                    cls.find_from_picture_book(game_state)
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
                print "You open the door and pop the hood then attach battery jumper to the battery terminals\n" \
                      "in the car. Upon turning the keys the dash lights up and the car starts.\n" \
                      "The car is now running and you remove the batter jumper."
            elif "carKey" in game_state.player.inventory and car.jumped is False:
                car.description = "A 90's Porsche 911. Too bad the battery is dead."
                print "You open the door and attempt to start the car, but the car does not start, nor does the dash\n" \
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
                main_gate.description = "The gate is wide open to the darkness beyond.\nYou probably don't want " \
                                        "to go out there; there might be killers and wolfs."
                print "Using the bolt cutter, you cut the chains off the gate and push the gate open to the endless\n" \
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
                    print "You drive the car out of the garage into the courtyard. Unfortunately, the gate is locked\n"\
                          "and you probably don't want to wreck the only vehicle into the hardened gates. You stepped\n"\
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
                    print "You drive the car through the gates, leaving this wrench house behind.\n" \
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
        piano = game_state.get_feature_by_name("piano")
        if piano.object:
            game_state.player.add_to_inventory(piano.object)
            piano.object = None
            print "You found a bolt cutter inside the piano. Might be useful."
        else:
            print "There's nothing in here."

    @classmethod
    def open_dresser(cls, game_state):
        dresser = game_state.get_feature_by_name("dresser")
        if dresser.object:
            game_state.player.add_to_inventory(dresser.object)
            dresser.object = None
            print "You found a car key inside the dresser! Looks like it's for a Porsche!"
        else:
            print "There's only clothes in here. They're not in your size."

    @classmethod
    def open_chest(cls, game_state):
        print "The chest is empty, but it has \"4624\" inscribed within the chest."

    @classmethod
    def open_pantry(cls, game_state):
        pantry = game_state.get_feature_by_name("pantry")
        if pantry.object:
            game_state.player.add_to_inventory(pantry.object)
            pantry.object = None
            print "You found a recipe book, titled ALL NATURAL."
            print "It does seem to have cooking recipes but herbal mixing formulas."
        else:
            print "There's nothing here but rotten food and a dead mouse."

    @classmethod
    def open_medicineCabinet(cls, game_state):
        medicine_cabinet = game_state.get_feature_by_name("medicineCabinet")
        if medicine_cabinet.object:
            game_state.player.add_to_inventory(medicine_cabinet.object)
            medicine_cabinet.object = None
            print "You found an antidote. It says it clears an intoxicated condition."
            print "But...it is up to you if you trust it or not."
        else:
            print "There's nothing else but deodorant and hair products."

    @classmethod
    def open_file_cabinet(cls, game_state):
        file_cabinet = game_state.get_feature_by_name("fileCabinet")
        if file_cabinet.object:
            game_state.player.add_to_inventory(file_cabinet.object)
            file_cabinet.object = None
            print "You found a family heirloom of a lion!"
        else:
            print "There is nothing interesting in this file cabinet."

    @classmethod
    def find_from_picture_book(cls, game_state):
        game_state.player.add_to_inventory("antidote")
        print "A card has dropped..."
        print "It seems that this book was a gift from ... Sloth Imai... who is it?"

    @classmethod
    def open_gun_safe(cls, game_state):
        gun_safe = game_state.get_feature_by_name("gunSafe")
        if gun_safe.object and gun_safe.locked:
            passcode = raw_input("Enter the 4-digit number: ")
            if passcode == "4624":
                game_state.player.add_to_inventory(gun_safe.object)
                gun_safe.object = None
                gun_safe.locked = False
                gun_safe.description = "The gun safe is unlocked."
                print "Beep! The safe unlocked and you found a handgun!"
            else:
                print "Access denied."
        else:
            print "There's nothing else in this gun safe."

    @classmethod
    def lift_bench(cls, game_state):
        game_state.player.add_to_inventory("carBatteryJumper")
        print "You found a car battery jumper!"

    @classmethod
    def familyName(cls, game_state, parsed_command):
        if parsed_command["familyName"] == "imai":
            game_state.player.add_to_inventory("masterKey")
            game_state.get_current_room().remove_feature("zombieSteward")
            print "You befriended the zombie. He gives you the master key and then disappears."

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

    @classmethod
    def make_life_potion(cls, game_state):
        metal_cabinet = game_state.get_feature_by_name("metalCabinet")
        if "recipeBook" in game_state.player.inventory:
            print "It seems that you have the recipe book, \"ALL NATURAL\"!"
            print "You might make something new! (press enter to leave)"
            metal_cabinet.status = "redPowder" #test: once metal cabinet is look-able, this will be deleted.
            if metal_cabinet.status == "redPowder":
                print "The red power you have is a sun stone powder. "
                print "Sun stone is a feldspar crystal that weathers out of certain lava flows in south-central Oregon."
                print "Let's distill it with water.\nYou've got a life potion."
                game_state.player.add_to_inventory("lifePotion")
                print "A life potion is added to your inventory. It will automatically revive you for once."
                metal_cabinet.status = "locked"
            elif metal_cabinet.status == "bluePowder":
                print "The blue power you have is a benitoite power."
                print "Benitoite gem stone is also called as a \"blue diamond\"."
                print "It is a rare kind of gem and only found in California."
                print "Let's distill it with water.\nOh no, it started smoking here..."
                print "You can't mix the water with non-local items..."
                game_state.player.status = "poisoned"
                print "Your health got recovered fully but poisoned by the blue smoke."
                # TODO : Do recover player's health to full
                metal_cabinet.status = "locked"
            elif metal_cabinet.status == "driedLeaves":
                print "The dried leaf was green tea leaves. You brewed green tea and sipped it. Not bad at all."
                metal_cabinet.status = "locked"
            else:
                print "You don't have no items to distill a potion."
        else:
            print "You don't know the book, \"ALL NATURAL\", do you?"
            print "You can't make anything. Don't waste your time here. Come back later."

    @classmethod
    def open_metal_cabinet(cls, game_state):
        metal_cabinet = game_state.get_feature_by_name("metalCabinet")
        if metal_cabinet.status == "locked":
            print "Somehow the metal cabinet got locked..."
        elif metal_cabinet.status in ["redPowder", "bluePowder", "driedLeaf"]:
            print "You already have selected one. Try to make a potion."
            cls.make_life_potion(game_state)
        else:
            print "There are a blue powder bottle, a red powder bottle and a dried leaves bottle in the each bottle."
            print "Which one do you need?"
            picked = False
            while not picked:
                picked_bottle = raw_input(">>")
                if picked_bottle == "":
                    print "Not interested? Never mind."
                    break
                elif picked_bottle.lower() in ["blue", "blue powder", "blue powder bottle", "a blue powder bottle",
                                               "a blue bottle"]:
                    metal_cabinet.status = "bluePowder"
                    picked = True
                elif picked_bottle.lower() in ["red", "red powder", "red powder bottle", "a red powder bottle",
                                               "a red bottle"]:
                    metal_cabinet.status = "redPowder"
                    picked = True
                elif picked_bottle.lower() in ["dried leaves", "dried leaves bottle", "a dried leaves bottle"]:
                    metal_cabinet.status = "driedLeaves"
                    picked = True
                else:
                    print "Re-enter the item you need. If you don't want any of items, press ENTER to close cabinet."
            if picked:
                cls.make_life_potion(game_state)

    @classmethod
    def endgame(cls, game_state, parsed_command):
        print "Thanks for playing, bye!"
        exit()

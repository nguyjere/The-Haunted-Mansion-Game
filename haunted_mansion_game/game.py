"""
Contains the main loop of the game and core functions
"""


def main_main():
    print "Title"
    print "Main Menu"
    print "[1] Start New Game"
    print "[2] Load Game"
    print "[3] Exit"
    return raw_input(">>")


def play():
    # game loop here
    while True:
        print "Displays current room description"
        print "Displays features and objects in the room"
        user_input = raw_input(">>")
        print "Parse and execute action with user input: {}".format(user_input)
        if user_input == "end game":
            print "You Died"
            break


def load_game(saved_game):
    print "Loading {0}...".format(saved_game)
    # loads player, room, and item data


def save_game():
    # saves player, room, and item data
    pass


def select_saved_games():
    print "Here's a list of saved games. Pick one"
    # display list of saved game files
    return raw_input(">>")


if __name__ == "__main__":
    menu_input = main_main()
    if menu_input == '1':
        play()
    elif menu_input == '2':
        selected_game_save = select_saved_games()
        load_game(selected_game_save)
        play()
    elif menu_input == '3':
        exit()

"""
Contains the main loop of the game and core functions
"""
from command_line_parser.textParser import *
from save_and_load import *
from utilities import *

global player
global rooms
global items


def main_main():
    print "Title"
    print "Main Menu"
    print "[1] Start New Game"
    print "[2] Load Game"
    print "[3] Exit"
    return raw_input(">>")


def select_saved_games():
    print "Here's a list of saved games. Pick one"
    # display list of saved game files
    return raw_input(">>")


def play():
    text_parser = TextParser()
    while True:
        current_room = get_room_by_name(player.currentRoom, rooms)
        # TODO: Print current room long, or short, description and display objects and features
        print "Displays current room description"
        print "Displays features and objects in the room"
        user_input = raw_input(">>")
        parsed_command = text_parser.getCommand(user_input, current_room)
        if parsed_command:
            # TODO: Pass parsed_command to a parsed_command_handler that will call an action
            print parsed_command
        else:
            print "I don't understand that"
        if user_input == "end game":
            print "You Died"
            break


if __name__ == "__main__":
    menu_input = main_main()
    if menu_input == '1':
        player, rooms, items = load_new_game()
    elif menu_input == '2':
        selected_game_save = select_saved_games()
        player, rooms, items = load_game(selected_game_save)
    elif menu_input == '3':
        exit()
    play()

"""
Contains the main loop of the game and core functions
"""
from command_line_parser.textParser import *
from game_state import *
from utilities import *


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


def play(game_state):
    text_parser = TextParser()
    game_state.display_current_room()
    while True:
        user_input = raw_input(">>")
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        if parsed_command:
            print parsed_command
            execute_action(parsed_command, game_state)
        else:
            print "I don't understand that"
        if user_input == "end game":
            print "You Died"
            break


if __name__ == "__main__":
    menu_input = main_main()
    if menu_input == '1':
        game = GameState()
        play(game)
    elif menu_input == '2':
        selected_game_save = select_saved_games()
        game = GameState(selected_game_save)
        play(game)
    elif menu_input == '3':
        exit()


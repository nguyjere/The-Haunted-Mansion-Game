"""
Contains the main loop of the game and core functions
"""
import sys
sys.path.append('../')
from command_line_parser.textParser import *
from game_state import *
import misc.miscDescriptions


def main_main():
    print "Welcome to The Haunted Python Mansion"
    print "Main Menu"
    print "[1] Start New Game"
    print "[2] Load Game"
    print "[3] Exit"
    return raw_input(">>")


def select_saved_games():
    print "Here's a list of saved games. Pick one"
    # display list of saved game files
    for file_name in os.listdir('../saved_games/'):
        if os.path.isdir("../saved_games/"+file_name) is True:
            print file_name
    # prompt player the file name and do file name input validation
    file_name_matched = False
    prompt_counter = 3
    while file_name_matched is False and prompt_counter > 0:
        selected_file_name = raw_input(">>")
        for file_name in os.listdir('../saved_games/'):
            if file_name == selected_file_name:
                return selected_file_name
        prompt_counter -= 1
        # if player enter unmatched name for 3 times, let one decide keep retrying or load new game
        if prompt_counter is 0:
            print "no matching game state found for 3 tries."
            print "retry to enter game state name? enter yes to retry. if not yes, will start new game."
            retry_yes_no = raw_input(">>")
            if retry_yes_no.lower() == "yes":
                prompt_counter = 3
            else:
                print retry_yes_no.lower()
                return None


def play(game_state):
    text_parser = TextParser()
    print misc.miscDescriptions.introduction
    game_state.display_current_room()
    while True:
        user_input = raw_input(">>")
        if user_input.lower().replace(" ","") == "loadgame":
            game_state = GameState(select_saved_games())
            game_state.display_current_room()
            continue
        parsed_command = text_parser.getCommand(user_input, game_state.get_current_room(), game_state.player)
        if parsed_command and "error" not in parsed_command.keys():
            if game_state.player.debug:
                print parsed_command
            game_state.execute_action(parsed_command)
        elif "error" in parsed_command.keys():
            print parsed_command["error"]
        else:
            print "I don't understand that"


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


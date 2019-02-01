class Actions:

    def __init__(self):
        pass

    @classmethod
    def go(cls, game_state, new_room_name):
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

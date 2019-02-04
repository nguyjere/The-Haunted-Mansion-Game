import unittest

from game import *


class TestTextParser(unittest.TestCase):

    def test_load_game(self):
        game_state = GameState()
        assert game_state is not None
        # Just make sure there's no error



from textParser import TextParser
from synonymRetriever import SynonymRetriever
import sys
sys.path.insert(0, '../haunted_mansion_game')
from room import *
from player import *

testRoomObj = Room("barLounge.json")

playerObj = Player("player.json")

textParser = TextParser()
#synonymRetriever = SynonymRetriever()
#synonymRetriever.synonymSwap("eat doll")

while True:

    command = textParser.promptUser('What? ')
    parsedCommand = textParser.getCommand(command, testRoomObj, playerObj)
    print parsedCommand
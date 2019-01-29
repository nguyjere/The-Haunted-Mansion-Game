from textParser import TextParser
import sys
sys.path.insert(0, '../haunted_mansion_game')
from room import *

testRoomObj = Room("barLounge.json")

textParser = TextParser()


while True:

    command = textParser.promptUser('Where to? ')
    parsedCommand = textParser.getCommand(command, testRoomObj)
    print parsedCommand

    command = textParser.promptUser('Look where? ')
    parsedCommand = textParser.getCommand(command, testRoomObj)
    print parsedCommand

    command = textParser.promptUser('What object? ')
    parsedCommand = textParser.getCommand(command, testRoomObj)
    print parsedCommand

    #command = textParser.promptUser('Where to? ')
    #parsedCommand = textParser.interpretRoom(command, testRoomObj)
    #print parsedCommand

    #command = textParser.promptUser('Look where? ')
    #parsedCommand = textParser.interpretLook(command, testRoomObj)
    #print parsedCommand

    ##command = textParser.promptUser('Where to? ')
    ##parsedCommand = textParser.preParseRoomCommand(command)
    ##print parsedCommand

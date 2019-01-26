from textParser import TextParser

textParser = TextParser(123)
while True:
    command = textParser.promptUser('Where to? ')
    parsedCommand = textParser.interpretRoom(command)
    print parsedCommand

    #command = textParser.promptUser('Look where? ')
    #parsedCommand = textParser.interpretLook(command)
    #print parsedCommand

    ##command = textParser.promptUser('Where to? ')
    ##parsedCommand = textParser.preParseRoomCommand(command)
    ##print parsedCommand

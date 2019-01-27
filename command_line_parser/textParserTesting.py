from textParser import TextParser
#
textParser = TextParser()
testRoomDict = {
  "roomName": "bar",
  "connectedTo": ["livingroom"],
  "displayRoomName": "Bar",
  "features": ["stools","pooltable", "barcounter", "cabinet", "frenchdoor"],
  "objects": ["winebottle"],
  "visited": "false"
}

while True:
    command = textParser.promptUser('Where to? ')
    parsedCommand = textParser.interpretRoom(command, testRoomDict)
    print parsedCommand

    command = textParser.promptUser('Look where? ')
    parsedCommand = textParser.interpretLook(command, testRoomDict)
    print parsedCommand

    ##command = textParser.promptUser('Where to? ')
    ##parsedCommand = textParser.preParseRoomCommand(command)
    ##print parsedCommand

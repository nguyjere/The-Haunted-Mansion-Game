import vocabulary
class TextParser:


    def __init__(self, gameId):
        self.gameId = gameId
        self.verbs = vocabulary.verbs
        self.rooms = vocabulary.rooms
        self.directions = vocabulary.directions
        self.features = vocabulary.features
        self.prepositions = vocabulary.prepositions

    def promptUser(self, prompt):
        command = raw_input(prompt)
        return command

    #parses commands
    def parseCommand(self, command):
        words = command.split()
        return words

    # parameters 
    # words: a command
    # interpretRoom, among other interpret commands can be used in a loop to figure out the user command
    # if interpretRoom returns a non-empty dictionary, then we know the user wants to go to a new room
    def interpretRoom(self, command):
        parsedWords = self.parseCommand(command)
        verb = self.findWord(parsedWords, "verb")
        room = self.findWord(parsedWords, "room")
        direction = self.findWord(parsedWords, "direction")
        userCommandDict = {"verb":verb, "room": room, "direction":direction}
        valid = self.errorCheckRoomCommand(userCommandDict)
        if valid != True:
            userCommandDict = {"verb": '', "room": '', "direction": ''}
        return userCommandDict

    # if just look is returned, then repeat description of room
    # if look at feature is returned, then describe feature
    def interpretLook(self, command):
        parsedWords = self.parseCommand(command)
        verb = self.findWord(parsedWords, "verb")
        feature = self.findWord(parsedWords, "feature")
        preposition = self.findWord(parsedWords, "preposition")
        userCommandDict = {"verb": verb, "feature": feature, "preposition": preposition}
        valid = self.errorCheckLookCommand(userCommandDict)
        if valid != True:
            userCommandDict = {"verb": '', "feature": '', "preposition": ''}
        return userCommandDict
            
    
    def findWord(self, words, type):
        foundWord = ""
        if type == "verb":
            listToSearch = self.verbs
        if type == "room":
            listToSearch = self.rooms
        if type == "direction":
            listToSearch = self.directions
        if type == "feature":
            listToSearch = self.features
        if type == "preposition":
            listToSearch = self.prepositions
        for word in words:
            for c in listToSearch:
                if word == c:
                    foundWord = c
                    break
        return foundWord
        

    def errorCheckRoomCommand(self, userCommandDict):
        if userCommandDict["verb"] == "go" and (userCommandDict["room"] != "" or userCommandDict["direction"] != ""):
            return True
        elif userCommandDict["verb"] == "" and (userCommandDict["room"] != "" or userCommandDict["direction"] != ""):
            return True
        else:
            return False

    def errorCheckLookCommand(self, userCommandDict):
        if userCommandDict["verb"] == "look" and userCommandDict["feature"] == "" and \
                userCommandDict["preposition"] == "":
            return True
        elif userCommandDict["verb"] == "look" and userCommandDict["feature"] != "" and \
                userCommandDict["preposition"] == "at":
            return True
        else:
            return False

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


    def parseCommand(self, command):
        words = command.split()
        return words

    '''
    interpretRoom, among other interpret commands can be used in a loop to figure out the user command
    if interpretRoom returns a non-empty dictionary, then we know the user wants to go to a new room
    '''

    def interpretRoom(self, command):
        parsedWords = self.parseCommand(command)
        verb = self.findWord(parsedWords, "verb")
        room = self.findWord(parsedWords, "room")
        direction = self.findWord(parsedWords, "direction")
        userCommandDict = {"verb":verb, "room": room, "direction":direction}
        valid = self.errorCheckRoomCommand(userCommandDict)
        if valid == True:
            userCommandDict = {"verb": verb["word"], "room": room["word"], "direction": direction["word"]}
        if valid != True:
            userCommandDict = {"verb": '', "room": '', "direction": ''}
        return userCommandDict

    '''
    if just look is returned, then repeat description of room
    if look at feature is returned, then describe feature
    '''
    def interpretLook(self, command):
        parsedWords = self.parseCommand(command)
        verb = self.findWord(parsedWords, "verb")
        feature = self.findWord(parsedWords, "feature")
        preposition = self.findWord(parsedWords, "preposition")
        userCommandDict = {"verb": verb, "feature": feature, "preposition": preposition}
        valid = self.errorCheckLookCommand(userCommandDict)
        if valid == True:
            userCommandDict = {"verb": verb["word"], "feature": feature["word"], "preposition": preposition["word"]}
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
        index = ""
        for word in words:
            for c in listToSearch:
                if word == c:
                    foundWord = c
                    index = words.index(foundWord)
                    break
        return {"word": foundWord, "index": index}
        
    '''
    go room, room, go direction, direction are valid
    everything else is not
    TO DO: check for extraneous words
    '''
    def errorCheckRoomCommand(self, userCommandDict):

        verb = userCommandDict["verb"]["word"]
        room = userCommandDict["room"]["word"]
        direction = userCommandDict["direction"]["word"]

        verbindex = userCommandDict["verb"]["index"]
        roomindex = userCommandDict["room"]["index"]
        directionindex = userCommandDict["direction"]["index"]

        if verb == "go" and room != "" and verbindex < roomindex:
            return True
        elif verb == "go" and direction != "" and verbindex < directionindex:
            return True
        elif verb == "" and room != "" and direction == "":
            return True
        elif verb == "" and room == "" and direction != "":
            return True
        else:
            return False

    '''
    look, look at feature are valid
    everything else is not
    TO DO: check for extraneous words
    '''
    def errorCheckLookCommand(self, userCommandDict):
        verb = userCommandDict["verb"]["word"]
        feature = userCommandDict["feature"]["word"]
        preposition = userCommandDict["preposition"]["word"]

        verbindex = userCommandDict["verb"]["index"]
        prepositionindex = userCommandDict["preposition"]["index"]
        featureindex = userCommandDict["feature"]["index"]

        if verb == "look" and feature == "" and preposition == "":
            return True
        elif verb == "look" and feature != "" and preposition == "at" and verbindex < prepositionindex < featureindex:
            return True
        else:
            return False

import vocabulary


class TextParser:

    def __init__(self):
        self.verbs = vocabulary.verbs
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
    Use this function in the execution engine to get back a dictionary that represents the parsed user command.
    '''
    def getCommand(self, command, roomObj):
        parsedRoomCommand = self.interpretRoom(command, roomObj)
        parsedFeatureCommand = self.interpretLook(command, roomObj)
        parsedObjectCommand = self.interpretTake(command, roomObj)

        finalParsedCommand = parsedRoomCommand.copy()
        finalParsedCommand.update(parsedFeatureCommand)
        finalParsedCommand.update(parsedObjectCommand)
        return finalParsedCommand

    '''
    normalizes words by making them lowercase
    finds features that may have space such as pool table and makes it one word, i.e. pooltable
    '''

    def preParseFeatureCommand(self, command):
        parsedWords = self.parseCommand(command)
        preParsedCommandList = []
        spaceFeatures = ["doll", "pool", "bar", "french",
                         "washing", "medicine", "garden", "garage",
                         "main", "dining", "china", "arched",
                         "tool", "back", "book", "fire", "front", "gun", "lab",
                         "file"]
        spaceFeaturesDict = {"doll": "house", "pool": "table", "bar": "counter", "french": "door",
                             "washing": "machine", "medicine": "cabinet", "garden": "gate", "garage": "door",
                             "main": "gate", "dining": "table", "china": "cabinet", "arched": "entryways",
                             "tool": "cabinet", "back": "door", "book": "shelf", "fire": "place", "front": "door",
                             "gun": "safe", "lab": "table", "file": "cabinet"}
        # make all words lowercase
        for word in parsedWords:
            preParsedCommandList.append(word.lower())
        for word in preParsedCommandList:
            if word in spaceFeatures:
                featureIndex = preParsedCommandList.index(word)
                if featureIndex + 1 <= len(preParsedCommandList) - 1:
                    if preParsedCommandList[featureIndex + 1] == spaceFeaturesDict[word]:
                        preParsedCommandList[featureIndex] = word + spaceFeaturesDict[word]
                        del preParsedCommandList[featureIndex + 1]
        return preParsedCommandList

    '''
    normalizes words by making them lowercase
    finds objects that may have spaces such as main gate lock and makes it one word, i.e. maingatelock
    '''

    def preParseObjectCommand(self, command):
        parsedWords = self.parseCommand(command)
        preParsedCommandList = []
        oneSpaceObjects = ["wine", "bolt", "recipe", "picture", "herb", "tea", "zombie", "family"]
        oneSpaceObjectsDict = {"wine":"bottle", "bolt":"cutter", "recipe":"book", "picture":"book",
                            "herb":"bottles", "tea":"kettle", "zombie":"steward", "family":"emblems"}
        twoSpaceObjects = ["old", "main", "car"]
        twoSpaceObjectsDict = {"old":"familypicture", "main":"gatelock", "car":"batteryjumper"}
        # make all words lowercase
        for word in parsedWords:
            preParsedCommandList.append(word.lower())
        for word in preParsedCommandList:
            if word in oneSpaceObjects:
                objectIndex = preParsedCommandList.index(word)
                if objectIndex + 1 <= len(preParsedCommandList) - 1:
                    if preParsedCommandList[objectIndex + 1] == oneSpaceObjectsDict[word]:
                        preParsedCommandList[objectIndex] = word + oneSpaceObjectsDict[word]
                        del preParsedCommandList[objectIndex + 1]
        for word in preParsedCommandList:
            if word in twoSpaceObjects:
                objectIndex = preParsedCommandList.index(word)
                if objectIndex + 1 <= len(preParsedCommandList) - 1 and objectIndex + 2 <= len(preParsedCommandList) - 1:
                    if preParsedCommandList[objectIndex + 1] + \
                            preParsedCommandList[objectIndex + 2] == twoSpaceObjectsDict[word]:
                        preParsedCommandList[objectIndex] = word + twoSpaceObjectsDict[word]
                        del preParsedCommandList[objectIndex + 1]
                        del preParsedCommandList[objectIndex + 1]
        return preParsedCommandList

    '''
    normalizes words by making them lowercase
    finds rooms that may have space such as dining room and makes it one word, i.e. diningroom
    '''

    def preParseRoomCommand(self, command):
        parsedWords = self.parseCommand(command)
        preParsedCommandList = []
        spaceRooms = ["dining", "guest", "living", "master", "secret", "steward"]
        # make all words lowercase
        for word in parsedWords:
            preParsedCommandList.append(word.lower())
        # diningroom guestroom livingroom masterbedroom secretroom stewardroom
        for word in preParsedCommandList:
            if word in spaceRooms:
                roomTypeIndex = preParsedCommandList.index(word)
                if roomTypeIndex + 1 <= len(preParsedCommandList) - 1:
                    if preParsedCommandList[roomTypeIndex + 1] == "room":
                        preParsedCommandList[roomTypeIndex] = word + "room"
                        del preParsedCommandList[roomTypeIndex + 1]
        return preParsedCommandList

    '''
    interpretRoom, among other interpret commands can be used in a loop to figure out the user command
    if interpretRoom returns a non-empty dictionary, then we know the user wants to go to a new room
    '''

    def interpretRoom(self, command, roomObj):
        connectedRooms = []
        for room in roomObj.connectedTo:
            connectedRooms.append(room.lower())
        parsedWords = self.preParseRoomCommand(command)
        verb = self.findWord(parsedWords, "verb", {})
        room = self.findWord(parsedWords, "room", connectedRooms)
        direction = self.findWord(parsedWords, "direction", {})
        userCommandDict = {"verb": verb, "room": room, "direction": direction}
        valid = self.errorCheckRoomCommand(userCommandDict)
        if valid == True:
            userCommandDict = {"verb": verb["word"], "room": room["word"], "direction": direction["word"]}
        if valid != True:
            userCommandDict = {}
        return userCommandDict

    '''
    if just look is returned, then repeat description of room
    if look at feature is returned, then describe feature
    '''

    def interpretLook(self, command, roomObj):
        availableFeatures = []
        for feat in roomObj.features:
            availableFeatures.append(feat.lower())
        parsedWords = self.preParseFeatureCommand(command)
        verb = self.findWord(parsedWords, "verb", {})
        feature = self.findWord(parsedWords, "feature", availableFeatures)
        preposition = self.findWord(parsedWords, "preposition", {})
        userCommandDict = {"verb": verb, "feature": feature, "preposition": preposition}
        valid = self.errorCheckLookCommand(userCommandDict)
        if valid == True:
            userCommandDict = {"verb": verb["word"], "feature": feature["word"], "preposition": preposition["word"]}
        if valid != True:
            userCommandDict = {}
        return userCommandDict

    '''
    if valid take command found, returns dictionary containing take verb and object user wishes to take
    else returns empty dictionary
    '''
    def interpretTake(self, command, roomObj):
        availableObjects = []
        for obj in roomObj.objects:
            availableObjects.append(obj.lower())
        parsedWords = self.preParseObjectCommand(command)
        verb = self.findWord(parsedWords, "verb", {})
        object = self.findWord(parsedWords, "object", availableObjects)
        userCommandDict = {"verb": verb, "object": object}
        valid = self.errorCheckObjectCommand(userCommandDict)
        if valid == True:
            userCommandDict = {"verb": verb["word"], "object": object["word"]}
        if valid != True:
            userCommandDict = {}
        return userCommandDict

    def findWord(self, words, type, listFromRoom):
        foundWord = ""
        if type == "verb":
            listToSearch = self.verbs
        if type == "room":
            listToSearch = listFromRoom
        if type == "direction":
            listToSearch = self.directions
        if type == "feature":
            listToSearch = listFromRoom
        if type == "preposition":
            listToSearch = self.prepositions
        if type == "object":
            listToSearch = listFromRoom
        index = ""
        for word in words:
            for c in listToSearch:
                if word == c:
                    foundWord = c
                    index = words.index(foundWord)
                    break
        return {"word": foundWord, "index": index}

    '''
    take object is valid. nothing else is.
    '''
    def errorCheckObjectCommand(self, userCommandDict):
        verb = userCommandDict["verb"]["word"]
        object = userCommandDict["object"]["word"]

        verbindex = userCommandDict["verb"]["index"]
        objectindex = userCommandDict["object"]["index"]

        if verb == "take" and object != "" and verbindex < objectindex:
            return True
        else:
            return False

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

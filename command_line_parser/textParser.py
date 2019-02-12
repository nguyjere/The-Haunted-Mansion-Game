import vocabulary
from synonymRetriever import *
from haunted_mansion_game.item import *

class TextParser:

    def __init__(self):
        self.verbs = vocabulary.verbs
        self.directions = vocabulary.directions
        self.features = vocabulary.features
        self.prepositions = vocabulary.prepositions
        self.ourcommands = vocabulary.ourcommands

    def promptUser(self, prompt):
        command = raw_input(prompt)
        return command

    def parseCommand(self, command):
        words = command.split()
        return words

    '''
    Use this function in the execution engine to get back a dictionary that represents the parsed user command.
    '''
    def getCommand(self, command, roomObj, playerObj):
        synonymRetriever1 = SynonymRetriever()
        command = synonymRetriever1.synonymSwap(command)
        parsedRoomCommand = self.interpretRoom(command, roomObj)
        parsedLookCommand = self.interpretLook(command, roomObj, playerObj)
        parsedObjectCommand = self.interpretTake(command, roomObj)
        parsedMetaCommand = self.interpretMeta(command, roomObj)
        parsedOurCommand = self.interpretOurCommand(command, roomObj, playerObj)

        finalParsedCommand = parsedRoomCommand.copy()
        finalParsedCommand.update(parsedLookCommand)
        finalParsedCommand.update(parsedObjectCommand)
        finalParsedCommand.update(parsedMetaCommand)
        finalParsedCommand.update(parsedOurCommand)
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
                         "file", "console", "car"]
        spaceFeaturesDict = {"doll": "house", "pool": "table", "bar": "counter", "french": "door",
                             "washing": "machine", "medicine": "cabinet", "garden": "gate", "garage": "door",
                             "main": "gate", "dining": "table", "china": "cabinet", "arched": "entryways",
                             "tool": "cabinet", "back": "door", "book": "shelf", "fire": "place", "front": "door",
                             "gun": "safe", "lab": "table", "file": "cabinet", "console": "table", "car": "key"}
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
        oneSpaceObjects = ["wine", "bolt", "recipe", "picture", "herb", "tea", "zombie", "family", "car"]
        oneSpaceObjectsDict = {"wine":"bottle", "bolt":"cutter", "recipe":"book", "picture":"book",
                            "herb":"bottles", "tea":"kettle", "zombie":"steward", "family":"emblems", "car":"key"}
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
        spaceDirections = ["north", "south"]

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

        for word in preParsedCommandList:
            if word in spaceDirections:
                directionIndex = preParsedCommandList.index(word)
                if directionIndex + 1 <= len(preParsedCommandList) - 1:
                    if preParsedCommandList[directionIndex + 1] == "west" or \
                            preParsedCommandList[directionIndex + 1] == "east":
                        preParsedCommandList[directionIndex] = word + preParsedCommandList[directionIndex + 1]
                        del preParsedCommandList[directionIndex + 1]

        return preParsedCommandList

    '''
    normalizes words by making them lowercase
    finds metacommands that may have space such as save game and makes it one word, i.e. savegame
    '''

    def preParseMetaCommand(self, command):
        parsedWords = self.parseCommand(command)
        preParsedCommandList = []
        spaceMeta = ["save", "load"]
        # make all words lowercase
        for word in parsedWords:
            preParsedCommandList.append(word.lower())
        # savegame loadgame
        for word in preParsedCommandList:
            if word in spaceMeta:
                metaIndex = preParsedCommandList.index(word)
                if metaIndex + 1 <= len(preParsedCommandList) - 1:
                    if preParsedCommandList[metaIndex + 1] == "game":
                        preParsedCommandList[metaIndex] = word + "game"
                        del preParsedCommandList[metaIndex + 1]
        return preParsedCommandList

    '''
    normalizes words by making them lowercase
    finds commands that may have space and makes them one word, i.e. turn on and turn off
    '''

    def preParseOurCommand(self, command):
        parsedWords = self.parseCommand(command)
        preParsedCommandList = []
        # make all words lowercase
        for word in parsedWords:
            preParsedCommandList.append(word.lower())
        # turn on turn off
        for word in preParsedCommandList:
            if word == "turn":
                ourcommandIndex = preParsedCommandList.index(word)
                if ourcommandIndex + 1 <= len(preParsedCommandList) - 1:
                    if preParsedCommandList[ourcommandIndex + 1] == "on" or \
                            preParsedCommandList[ourcommandIndex + 1] == "off" :
                        preParsedCommandList[ourcommandIndex] = word + preParsedCommandList[ourcommandIndex + 1]
                        del preParsedCommandList[ourcommandIndex + 1]
        return preParsedCommandList

    def translateDirectionToRoom(self, roomObj, userCommandDict):
        if userCommandDict["direction"]["word"] != "" and userCommandDict["room"]["word"] == "":
            validDirection = False
            for key in roomObj.directions:
                if userCommandDict["direction"]["word"] == key:
                    validDirection = True
            if validDirection == True:
                userCommandDict["room"]["word"] = roomObj.directions[userCommandDict["direction"]["word"]]
                userCommandDict["room"]["index"] = userCommandDict["direction"]["index"]
                userCommandDict["direction"]["word"] = ""
                userCommandDict["direction"]["index"] = ""
            else:
                userCommandDict["direction"]["word"] = ""
                userCommandDict["direction"]["index"] = ""
                userCommandDict["verb"]["word"] = ""
                userCommandDict["verb"]["index"] = ""
                userCommandDict["room"]["word"] = ""
                userCommandDict["room"]["index"] = ""

    '''
    interpretRoom, among other interpret commands can be used in a loop to figure out the user command
    if interpretRoom returns a non-empty dictionary, then we know the user wants to go to a new room
    takes both roomObj and playerObj as parameters because a player can use our commands on features/objects in rooms
    and objects in a player's inventory
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
        self.translateDirectionToRoom(roomObj, userCommandDict)
        valid = self.errorCheckRoomCommand(userCommandDict)
        if valid == True:
            userCommandDict = {"verb": verb["word"], "room": room["word"], "direction": direction["word"]}
        if valid != True:
            userCommandDict = {}
        return userCommandDict

    '''
    interpretMeta, among other interpret commands can be used in a loop to figure out the user command
    if interpretMeta returns a non-empty dictionary, then we know the user wants: help, inventory, savegame, or 
    loadgame
    '''

    def interpretMeta(self, command, roomObj):
        parsedWords = self.preParseMetaCommand(command)
        verb = self.findWord(parsedWords, "verb", {})
        userCommandDict = {"verb": verb}
        valid = self.errorCheckMetaCommand(userCommandDict)
        if valid == True:
            userCommandDict = {"verb": verb["word"]}
        if valid != True:
            userCommandDict = {}
        return userCommandDict

    '''
       interpretOurCommands, among other interpret commands can be used in a loop to figure out the user command
       if interpretMeta returns a non-empty dictionary, then we know the user wants to use one of our unique commands:
       lift, drop, push, pull, consume, open, close, turn on, turn off, hit
       
       To do: should also accept playerObj as parameter because player can perform commands on objects in their 
       inventory
       '''

    def interpretOurCommand(self, command, roomObj, playerObj):
        availableFeatures = []
        compatibleCommands = {}
        for feat in roomObj.features:
            availableFeatures.append(feat.lower())
        availableObjects = []
        for obj in roomObj.objects:
            availableObjects.append(obj.lower())
        for obj in playerObj.inventory:
            availableObjects.append(obj.lower())
            # create dictionary mapping compatible commands to item
            item = Item(obj+".json")
            compatibleCommands[obj.lower()] = item.ourCompatibleCommands

        # to do: refactor this section of code
        parsedWords1 = self.preParseOurCommand(command)
        str1 = ' '.join(str(e) for e in parsedWords1)
        parsedWords2 = self.preParseFeatureCommand(str1)
        str2 = ' '.join(str(e) for e in parsedWords2)
        parsedWords3 = self.preParseObjectCommand(str2)
        parsedWords = parsedWords3
        #

        verb = self.findWord(parsedWords, "ourcommands", {})
        object = self.findWord(parsedWords, "object", availableObjects)
        feature = self.findWord(parsedWords, "feature", availableFeatures)
        userCommandDict = {"verb": verb, "object": object, "feature": feature}
        valid = self.errorCheckOurCommand(userCommandDict, compatibleCommands)
        if valid == True:
            userCommandDict = {"verb": verb["word"], "object": object["word"], "feature": feature["word"]}
        if valid != True:
            userCommandDict = {}
        return userCommandDict

    '''
    if just look is returned, then repeat description of room
    if look at feature is returned, then describe feature
    '''

    def interpretLook(self, command, roomObj, playerObj):
        availableFeatures = []
        for feat in roomObj.features:
            availableFeatures.append(feat.lower())
        availableObjects = []
        for obj in roomObj.objects:
            availableObjects.append(obj.lower())
        for obj in playerObj.inventory:
            availableObjects.append(obj.lower())
        parsedWords1 = self.preParseFeatureCommand(command)
        str1 = ' '.join(str(e) for e in parsedWords1)
        parsedWords2 = self.preParseObjectCommand(str1)
        verb = self.findWord(parsedWords2, "verb", {})
        feature = self.findWord(parsedWords2, "feature", availableFeatures)
        preposition = self.findWord(parsedWords2, "preposition", {})
        object = self.findWord(parsedWords2, "object", availableObjects)
        userCommandDict = {"verb": verb, "feature": feature, "preposition": preposition, "object": object}
        valid = self.errorCheckLookCommand(userCommandDict)
        if valid == True:
            userCommandDict = {"verb": verb["word"], "feature": feature["word"], "preposition": preposition["word"],
                               "object": object["word"]}
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
        if type == "ourcommands":
            listToSearch = self.ourcommands
        index = ""
        for word in words:
            for c in listToSearch:
                if word == c:
                    if index == "":
                        foundWord = c
                        index = words.index(foundWord)
                        break
                    else:
                        return {"word": "", "index": ""}
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
    help, inventory, savegame, loadgame are valid. nothing else is.
    '''
    def errorCheckMetaCommand(self, userCommandDict):
        verb = userCommandDict["verb"]["word"]
        if verb == "help" or verb == "inventory" or verb == "savegame" or verb == "loadgame":
            return True
        else:
            return False

    '''
    one of our unique commands, plus a feature XOR object.
    verb validation not needed here because only vocabulary.ourcommands is searched
    
    To do: more advanced implementation that limits which of our commands can be performed on which objects
    For example, you obviously cannot each a french door. We should check for things like this here.
    '''
    def errorCheckOurCommand(self, userCommandDict, compatibleCommands):
        verb = userCommandDict["verb"]["word"]
        feature = userCommandDict["feature"]["word"]
        object = userCommandDict["object"]["word"]

        verbindex = userCommandDict["verb"]["index"]
        featureindex = userCommandDict["feature"]["index"]
        objectindex = userCommandDict["object"]["index"]

        if verb != "" and object != "" and verb not in compatibleCommands[object]:
            return False

        if verb != "" and feature != "" and object == "" and verbindex < featureindex:
            return True
        elif verb != "" and object != "" and feature == "" and verbindex < objectindex:
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

        if room != "" and direction != "" and verb != "":
            return False
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
    look, look at feature, and look at object are valid
    everything else is not
    TO DO: check for extraneous words
    '''

    def errorCheckLookCommand(self, userCommandDict):
        verb = userCommandDict["verb"]["word"]
        feature = userCommandDict["feature"]["word"]
        preposition = userCommandDict["preposition"]["word"]
        object = userCommandDict["object"]["word"]

        verbindex = userCommandDict["verb"]["index"]
        prepositionindex = userCommandDict["preposition"]["index"]
        featureindex = userCommandDict["feature"]["index"]
        objectindex = userCommandDict["object"]["index"]

        if verb == "look" and feature == "" and object == "" and preposition == "":
            return True
        elif verb == "look" and feature != "" and object == "" \
                and preposition == "at" and verbindex < prepositionindex < featureindex:
            return True
        elif verb == "look" and feature == "" and object != "" \
                and preposition == "at" and verbindex < prepositionindex < objectindex:
            return True
        else:
            return False

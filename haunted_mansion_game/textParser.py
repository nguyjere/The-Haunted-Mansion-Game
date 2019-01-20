class TextParser:

    rooms = ["attic", "bar", "basement", "diningroom", "garage", "garden", "guestroom", "kitchen", "library", "livingroom", "lounge", "masterbedroom", "secretroom", "stewardsroom"] 

    verbs = ["look", "go", "take", "help", "inventory", "savegame", "loadgame", "lift", "drop", "push", "pull", "consume", "open", "close", "turnon", "turnoff", "hit"]

    directions = ["north", "south", "east", "west"]

    def _init_(self, gameId):
        self.gameId = gameId

    def promptUser(self, prompt):
        command = raw_input(prompt)
        return command

    def parseCommand(self, command):
        words = command.split()
        return words

    # parameters 
    # words: a list of words that represents that command
    def interpretBasic(self, words):
        verb = findWord(words, "verb")
        room = findWord(words, "room")
        userCommand = (verb, room)

        valid = errorCheckRoomCommand(userCommand)

        if valid == true:
            return userCommand
        else:
            return "Invalid Command"
            
    
    def findVerb(self, word, type):
        foundWord = ""
        if type == "verb":
            listToSearch = self.verbs
        if type == "room":
            listToSearch = self.rooms
        for word in words:
            for c in listToSearch:
                if word == c:
                    foundWord = c
                    break
        return foundWord
        

    def errorCheckRoomCommand(self, userCommand):
        if userCommand[0] == "go" and userCommand[1] != "":
            return true
        elif userCommand[0] == "" and userCommand[1] != "":
            return true
        else:
            return false

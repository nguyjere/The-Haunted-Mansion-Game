class TextParser:

    rooms = ["attic", "bar", "basement", "diningroom", "garage", "garden", "guestroom", "kitchen", "library", "livingroom", "lounge", "masterbedroom", "secretroom", "stewardsroom"] 

    verbs = ["look", "go", "take", "help", "inventory", "savegame", "loadgame", "lift", "drop", "push", "pull", "consume", "open", "close", "turnon", "turnoff", "hit"]

    directions = ["north", "south", "east", "west"]

    def _init_(self, gameId):
        self.gameId = gameId

    def promptUser(self, prompt):
        command = raw_input(prompt)
        return command
    #parses commands
    def parseCommand(self, command):
        words = command.split()
        return words

    # parameters 
    # words: a command
    def interpretBasic(self, command):
        parsedWords = self.parseCommand(command)
        verb = self.findWord(parsedWords, "verb")
        room = self.findWord(parsedWords, "room")
        direction = self.findWord(parsedWords, "direction")
        
        userCommandDict = {"verb":verb, "room": room, "direction":direction}
        valid = self.errorCheckRoomCommand(userCommandDict)
        
        if valid == True:
            return userCommandDict
        else:
            return "Invalid Command"
            
    
    def findWord(self, words, type):
        foundWord = ""
        if type == "verb":
            listToSearch = self.verbs
        if type == "room":
            listToSearch = self.rooms
        if type == "direction":
            listToSearch = self.directions
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

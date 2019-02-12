import vocabulary
#import requests
import synonyms

class SynonymRetriever:
    def __init__(self):
        self.verbs = vocabulary.verbs
        self.ourcommandsSpaced = vocabulary.ourcommandsSpaced
        self.synonyms = synonyms.synonyms

        # remove any of our commands from the synonyms lists
        for key, list in self.synonyms.iteritems():
            for word in list:
                if word in self.verbs or word in self.ourcommandsSpaced:
                    list.remove(word)

    def getSynonym(self, verb):
        return self.synonyms[verb]

    def synonymSwap(self, command):
        commandAsList = command.split()
        for key, list in self.synonyms.iteritems():
            for word in list:
                if word in commandAsList:
                    command = command.replace(word, key)
        return command
import vocabulary
#import requests
import synonyms

class SynonymRetriever:
    def __init__(self):
        self.verbs = vocabulary.verbs
        self.ourcommandsSpaced = vocabulary.ourcommandsSpaced
        #self.synonyms = {}
        self.synonyms = synonyms.synonyms

        # getting it from the web on the fly is pretty slow, it's much faster to hardcode in synonyms.py
        # for command in self.ourcommandsSpaced:
        #     url = 'http://words.bighugelabs.com/api/2/68117b8ed3008c3c79295c7c552364bf/' + command + '/json'
        #     response = requests.post(url)
        #     self.synonyms[command] = response.json()['verb']['syn']
        # print self.synonyms

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
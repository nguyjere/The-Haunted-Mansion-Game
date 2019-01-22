from textParser import TextParser

textParser = TextParser()

command = textParser.promptUser('Where to? ')
parsedCommand = textParser.interpretBasic(command)
print parsedCommand

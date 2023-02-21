import string
from random import randrange

class Random:
    def __init__(self):
        self.listOfLetters = list(string.ascii_lowercase)

    def runAlgorithm(self, phrase, guessedLetters):
        guessLetter = None
        while guessLetter == None:
            letterIndex = randrange(26)
            letter = self.listOfLetters[letterIndex]
            if letter not in guessedLetters:
                guessLetter = letter

        return guessLetter
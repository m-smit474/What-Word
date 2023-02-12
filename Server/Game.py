# Game.py
# Author: Matthew Smith @m-smit474
import random

class Game:
    def __init__(self, difficulty):            
        self.easyPhrases = []
        self.normalPhrases = []
        self.hardPhrases = []
        self.phrase = ""
        self.hidden = ""
        self.guessedLetters = set()       # set of guessed letter
        self.guessedWords = set()          # set of guessed words
        self.complete = False
        self.lives = 10
        self.score = 0
        self.scoreMultiplier = 1
        self.readFile()
        self.createPhrase(difficulty)
        self.coverPhrase()

    def restart(self):
        self.guessedLetters = set()       # set of guessed letter
        self.guessedWords = set()          # set of guessed words
        self.complete = False
        self.scoreMultiplier = 1
        self.lives = 10
        self.score = 0
        self.hidden = ""
        self.coverPhrase()
        

    def readFile(self):
        file = open("Phrases.txt", "r")
    
        for line in file:
            # Skip blank lines
            if len(line) > 1:
                # Easy Phrases
                if len(line.split()) <= 2:
                    self.easyPhrases.append(line)
                elif len(line.split()) <= 5:
                    self.normalPhrases.append(line)
                else:
                    self.hardPhrases.append(line)
            
        file.close()
    
    def createPhrase(self, difficulty):
        
        if difficulty == '1':
            randomIndex = random.randint(0, len(self.easyPhrases))
            self.phrase = self.easyPhrases[randomIndex]
        elif difficulty == '2':
            randomIndex = random.randint(0, len(self.normalPhrases))
            self.phrase = self.normalPhrases[randomIndex]
        elif difficulty == '3':
            randomIndex = random.randint(0, len(self.hardPhrases))
            self.phrase = self.hardPhrases[randomIndex]
        else:
            raise ValueError("Invalid difficulty: ", difficulty)

            

    def coverPhrase(self):
        for i in range(len(self.phrase)):
            if self.phrase[i].isalpha():
                self.hidden += '_'
            elif self.phrase[i] != '\n':
                self.hidden += self.phrase[i] 

    def guessLetter(self, letter):
        found = False
        points = 0
        letterCount = 0
        for i in range(len(self.phrase)):
            # for each letter in phrase check if it makes letter guessed
            if self.phrase[i].lower() == letter.lower() and letter not in self.guessedLetters:
                # Replace blank in hidden with letter
                self.hidden = self.hidden[:i] + self.phrase[i] + self.hidden[i + 1:]
                found = True
                

                # Add points for letter
                letterCount += 1
                points += (5 * letterCount)

        points = points * self.scoreMultiplier
        self.score += points 
        self.guessedLetters.add(letter)
        
        if not found:
            # Lose a life
            self.lives -= 1
            # Score multiplier resets
            self.scoreMultiplier = 1
        elif self.scoreMultiplier < 3:
            # Score multiplier increases up to three
            self.scoreMultiplier += 1

        if not self.hidden.__contains__('_'):
            self.complete = True

    def guessPhrase(self, phrase):
        if self.phrase.lower() == phrase.lower():
            self.hidden = self.phrase
            self.complete = True

            # Add score for winning game
            # Blank spots earn 50 points
            numberOfBlanks = self.hidden.count('_')
            self.score += (numberOfBlanks * 50)

            # Remaining lives earn 100 points
            self.score += (self.lives * 100)
        else:
            self.lives -= 1

    def isOutOfLives(self):
        out = False
        if self.lives <= 0:
            out = True
            self.score = self.score / 2

        return out
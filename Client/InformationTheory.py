# Create a frequency distribution for each letter using the word_frequency data set

import pandas as pd
import string

class InformationTheory:

    global totalLetterCount

    def __init__(self):
        self.wordFrequencyDF = pd.read_csv('English_Word_Frequency/word_frequency.csv')
        self.frequencyDistribution = self.createFrequencyDistribution()
        self.frequencyDistributionDF = pd.DataFrame({'Letter':list(self.frequencyDistribution.keys()),
        'Frequency':list(self.frequencyDistribution.values())}).sort_values('Frequency', ascending=False)

    def runAlgorithm(self, phrase, guessedLetters):
        # Guess the letters with the highest frequencies
        for rowInDF in self.frequencyDistributionDF.iterrows():
            letter = rowInDF[1]['Letter']
            if letter not in guessedLetters:
                outputLetter = letter
                break
        return outputLetter
        

    def createFrequencyDistribution(self):
        global totalLetterCount
        letterCount = self.createLetterOccurancesMap()
        frequecyDistribution = {letter : count/totalLetterCount for letter,count in letterCount.items()}
        return frequecyDistribution

        

    def createLetterOccurancesMap(self):
        # Create letter occurances dictionary
        global totalLetterCount 
        totalLetterCount = 0
        self.wordFrequencyDF.reset_index()
        letterCount = dict((key, 0) for key in string.ascii_lowercase)
        for rowInDF in self.wordFrequencyDF.head(10000).iterrows():

            highFrequencyWord = rowInDF[1]['word']

            if not isinstance(highFrequencyWord, float):
                for letter in highFrequencyWord:
                    count = letterCount.get(letter)
                    letterCount.update({letter : count + 1})
                    totalLetterCount = totalLetterCount + 1
        
        return letterCount
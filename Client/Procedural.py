#Procedural.py
#Author m-smit474
# This class is for the procedural algorithm which 'plays' the game 'What Word?!' defined in Game.py
# Algorithm 1:
# Very basic - Use word frequency data
# Assumption: Some letter will be found, because by the time all letters have been guessed the game must have complete.
"""
while letter not found:
    go through list of most common English words
    for each word in list:
        for each letter in word:
            if letter has not been guessed:
                letter found - return letter
"""

# Algorithm 2
# Iteration on 1 - only use words that match the size of words in phrase
# This algorithm will go through a list of the most common English words. It will try to find words that have the same
# length as words in the phrase, then use the letters of those words.
"""
while letter not found:
    go through list of most common English words
    for each word in list:
        if word length matches atleast one word length in phrase:
            for each letter in word:
                if letter has not been guessed:
                    letter found - return letter
"""
import pandas as pd

class Procedural:
    def __init__(self):
        self.wordFrequencyDF = pd.read_csv('English_Word_Frequency/word_frequency.csv')

    def runAlgorithm(self, phrase, guessedLetters):
        outputLetter = None
        self.wordFrequencyDF.reset_index()
        for rowInDF in self.wordFrequencyDF.iterrows():
            if outputLetter:
                break

            highFrequencyWord = rowInDF[1]['word']
            highFrequencyWordLength = rowInDF[1]['word_length']
            wordsInPhrase = mapWordsToSize(phrase)
            for wordInPhrase in wordsInPhrase:
                if highFrequencyWordLength == len(wordInPhrase):
                    for letter in highFrequencyWord:
                        if letter not in guessedLetters:
                            outputLetter = letter
                            return outputLetter

        return outputLetter

def mapWordsToSize(sentence):
    wordsInSentence = sentence.split()
    mapOfWordsSize = {}
    for word in wordsInSentence:
        mapOfWordsSize.update({word:len(word)})

    return mapOfWordsSize
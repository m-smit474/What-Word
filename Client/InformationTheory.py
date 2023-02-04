import pandas as pd

class InformationTheory:
    def __init__(self):
        self.wordFrequencyDF = pd.read_csv('English_Word_Frequency/word_frequency.csv')

    def runAlgorithm(self, phrase, guessedLetters):
        outputLetter = None
        """
        self.wordFrequencyDF.reset_index()
        for rowInDF in self.wordFrequencyDF.iterrows():
            if outputLetter:
                break
        """
        outputLetter = 'a'
        return outputLetter
        
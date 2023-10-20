import os.path
import string
import pandas as pd
import numpy as np
import random

# Index for each state
START = 0
CORRECT = 1
INCORRECT = 2

class QLearning:

    def __init__(self):
        self.lettersInAlphabet = list(string.ascii_lowercase)
        self.epsilon = 0.8          # How much exploring vs exploiting to do, high value = high exploring
        self.gamma = 0.3            # The importance of future rewards vs current reward, high value = more importance for future reward
        self.learningRate = 0.9     # How much new information overrides old information
        self.reward = 0
        self.availableStates = ['start', 'correct', 'incorrect']
        self.state = self.availableStates[START]
        self.previousPhrase = None
        self.filePath = "./QTable_Data/Second_QTable.csv"
        self.checkTable()

    def __init__(self, filename):
        self.lettersInAlphabet = list(string.ascii_lowercase)
        self.epsilon = 0.1          # How much exploring vs exploiting to do, high value = high exploring
        self.gamma = 0.3            # The importance of future rewards vs current reward, high value = more importance for future reward
        self.learningRate = 0.9     # How much new information overrides old information
        self.reward = 0
        self.availableStates = ['start', 'correct', 'incorrect']
        self.state = self.availableStates[START]
        self.previousPhrase = None
        self.filePath = "./QTable_Data/" + filename +".csv"
        self.checkTable()


    def tuneParameters(self):
        self.epsilon = self.epsilon - 0.1
        self.gamma = self.gamma + 0.1

    def runAlgorithm(self, phrase, guessedLetters):
        guessLetter = None

        if self.previousPhrase:
            self.previousState = self.state
            self.updateState(phrase)
            self.updateTable()

        # Epsilon determines how much exploring to do
        if random.uniform(0, 1) < self.epsilon:
            """
            Explore: select a random action    
            """
            while guessLetter == None:
                randomIndex = random.randint(0, len(self.lettersInAlphabet) - 1)
                letter = self.lettersInAlphabet[randomIndex]

                if letter not in guessedLetters:
                    guessLetter = letter
        else:
            """
            Exploit: select the action with max value (future reward)   
            """
            # The row of actions corresponding to the current state
            actionsForState = self.qTable.iloc[self.stateToIndex(self.state)]
            while guessLetter == None:
                # Find action with highest predicted reward
                action = actionsForState.idxmax(axis=1)

                # If action is already guessed, remove it from actions
                if action in guessedLetters:
                    actionsForState = actionsForState.drop(labels=action)
                else:
                    guessLetter = action

        self.previousLetter = guessLetter
        self.previousPhrase = phrase 

        return guessLetter
    
    def updateTable(self):
        # Update the Q-table value for the previous state and action based on the measured outcome/reward
        currentQValue = self.qTable.at[self.stateToIndex(self.previousState), self.previousLetter]
        temporalDifference = self.reward + self.gamma * np.max(self.qTable.iloc[self.stateToIndex(self.state), :]) - currentQValue
        newQValue = currentQValue + self.learningRate * temporalDifference
        self.qTable.at[self.stateToIndex(self.previousState), self.previousLetter] = newQValue
        self.qTable.to_csv(self.filePath, index=False)

    def stateToIndex(self, state):
        count = 0
        for potentialState in self.availableStates:
            if state == potentialState:
                index = count
            count = count + 1
        return index

        
    
    def updateState(self, phrase):
        blankCount = phrase.count("_")
        previousBlankCount = self.previousPhrase.count("_")
        if blankCount > previousBlankCount:
            self.state = self.availableStates[START]
            self.reward = 0
        elif blankCount < previousBlankCount:
            self.state = self.availableStates[CORRECT]
            self.reward = 1
        else:
            self.state = self.availableStates[INCORRECT]
            self.reward = -1


    def checkTable(self):
        if os.path.isfile(self.filePath):
            # read csv and initialize table variable
            self.qTable = pd.read_csv(self.filePath)
        else:
            # Q table not found - create new table
            self.qTable = self.createTable()
            self.qTable.to_csv(self.filePath, index=False)
            self.qTable = pd.read_csv(self.filePath)

    def createTable(self):
        states = self.availableStates
        actions = self.lettersInAlphabet

        # initialize action q-values to 0 for each state
        data = {}
        for action in actions:
            data.update({action:[0.0, 0.0, 0.0]})

        return pd.DataFrame(data, index=states)
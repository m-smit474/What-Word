# Client.py
# Author: Matthew Smith @m-smit474

import socket
import sys
import PySimpleGUI as sg
import pandas as pd
import random
import re
from Window import EXIT_BUTTON, window
from Procedural import Procedural
from InformationTheory import InformationTheory
from Random import Random
from QLearning import QLearning
from datetime import datetime
from csv import writer

# Standard loopback interface address 127.0.0.1
PORT = 6789         # Port number 

# Comparison Parameters
PAUSE = 600         # How long to wait during comparison guesses
ITERATIONS = 500  # How many times to run the comparison
ALGORITHMS = [QLearning("QTable2000"), Random(), InformationTheory(), Procedural()]

def main():
    # Create a socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        # Connect to server
        try:
            HOST = "127.0.0.1"
            clientSocket.connect((HOST,PORT))
        except ConnectionRefusedError:
                # No server found
            displayNoServerMessage()
            sys.exit(1)
        except TimeoutError:
                # No server found
            displayNoServerMessage()
            sys.exit(1)

        # Check for command line arguments
        if len(sys.argv) == 2 and sys.argv[1] == 'compare':
            window.read(PAUSE)
            comparison = Comparison(clientSocket)
            comparison.compare(ALGORITHMS, ITERATIONS)
        elif len(sys.argv) == 3 and sys.argv[1] == 'compare' and sys.argv[2].isnumeric:
            window.read(PAUSE)
            comparison = Comparison(clientSocket)
            comparison.compare(ALGORITHMS, int(sys.argv[2]))
        else: 
            client = Client(clientSocket)
            client.clientLoop()
                
            
        clientSocket.sendall(("exit").encode())
        window.close()

def displayNoServerMessage():
    sg.PopupError("No server found\n",
    "Please try again later or host the server.")

def displayNoGameRunningMessage():
    sg.popup_no_buttons('Start a new game!')

class Client:
    def __init__(self, clientSocket):
        self.clientSocket = clientSocket

    def parseInput(self, rawInput):
        output = None
        tokens = rawInput.split(" ")


        if len(tokens) == 1:
            if tokens[0].lower() == 'exit':
                output = "exit"
        elif len(tokens) == 2:
            if tokens[0].lower() == 'end' and tokens[1].lower() == 'game':
                output = "end game"
            elif tokens[0].lower() == 'guess':
                if not tokens[1].isalnum():
                    print("Guess contains invalid characters")
                    return None
                output = "guess " + tokens[1]
            else:
                print("Invalid command (2 tokens)")
        elif len(tokens) >= 3:
            # Start Game <Diffifulty>
            if tokens[0].lower() == 'start' and tokens[1].lower() == 'game' and tokens[2].isnumeric():
                if int(tokens[2]) <= 10 and int(tokens[2]) > 0:
                    output = "start game " + tokens[2]
                else:
                    print("Invalid difficulty! Must be 1-10")
            elif tokens[0].lower() == 'guess':
                output = ""
                for i in range(len(tokens) - 1):
                    if not tokens[i].isalnum():
                        print("Guess contains invalid characters")
                        return None

                    output += (tokens[i] + " ")
                    
                output += tokens[i + 1]
            else:
                print("Invalid command (3 tokens)")

                
        return output

    def getDifficulty(self):
        text = None

        
        text = sg.popup_get_text('Enter difficulty between 1-3')

        if text and not(text.isnumeric() and int(text) >= 1 and int(text) <= 3) :
            text = None

        return text

    def updateWindow(self, command):
        global running
        global phrase
        global guessedLetters
        global lives
        global score

        # Send message to server
        self.clientSocket.sendall(command.encode())

        # Not guaranteed to read entire message
        inFromServer = self.clientSocket.recv(1024).decode()
        clientOutput = inFromServer #.lstrip('b')

        try:
            update = clientOutput.split("@")[0]
            lives = clientOutput.split("@")[1].split(" ")[0]
            score = clientOutput.split("@")[1].split(" ")[1]
            running = clientOutput.split("@")[1].split(" ")[2]
            guessedLetters = clientOutput.split("@")[1].split(" ", 3)[3].replace("'","")
        except IndexError:
            raise ConnectionError("Server response error")

        if guessedLetters == 'set()':
            guessedLetters = ''

        window["_DISPLAY_"].update(update)
        window["-SCORE-"].update(score)
        window["-LIVES-"].update(lives)
        window["-GUESSED-"].update(guessedLetters)
        window["-GUESS-"].update("")

        phrase = update

    def procedural(self):
        clicked = sg.popup_ok_cancel('Do you want to run the word frequency algorithm?')

        if clicked == 'OK':
            self.runAlgorithm(Procedural())
    
    def random(self):
        clicked = sg.popup_ok_cancel('Do you want to run the random letter algorithm?')

        if clicked == 'OK':
            self.runAlgorithm(Random())

    def reinforcementLearning(self):
        clicked = sg.popup_ok_cancel('Do you want to run the reinforcement learning algorithm?')

        if clicked == 'OK':
            self.runAlgorithm(QLearning())

    def informationTheory(self):
        clicked = sg.popup_ok_cancel('Do you want to run the letter frequency algorithm?')

        if clicked == 'OK':
            self.runAlgorithm(InformationTheory())

    def runAlgorithm(self, algorithm):
        global lettersUsed
        lettersUsed = []
        while running == 'True':

            event, values = window.read(PAUSE)

            # End program if user closes window
            if event == "Exit" or event == EXIT_BUTTON:
                break

            guessLetter = algorithm.runAlgorithm(phrase, guessedLetters)
            lettersUsed.append(guessLetter)
            self.updateWindow('guess ' + guessLetter)

    def clientLoop(self):
        global running
        running = 'False'
        isRestartable = False

        # Client loop
        while True:
            event, values = window.read()

            # End program if user closes window
            if event == "Exit" or event == EXIT_BUTTON:
                break
            # Letters entered into guess bar
            if event == '-GUESS-':
                """
                guess = values['-GUESS-']
                update = guess
                """
            # Guess button clicked
            if event == 'Guess!':
                # ToDo error check here
                if running != 'True':
                    displayNoGameRunningMessage()
                else:
                    # Single character guesses must be a letter
                    if len(str(values['-GUESS-'])) == 1 and not str(values['-GUESS-'])[0].isalpha():
                            sg.popup_no_buttons('Invalid Guess: ' + str(values['-GUESS-']),title="Invalid Guess")
                    else:
                        self.updateWindow("guess " + str(values['-GUESS-']))
            # New game button clicked
            if event == 'NEW GAME':
                dif = self.getDifficulty()

                if dif:
                    isRestartable = True
                    self.updateWindow("start game " + str(dif))


            # Restart button clicked
            if event == 'Restart':
                # You can only restart a game if one has already started
                if isRestartable:
                    clicked = sg.popup_ok_cancel('Do you want to restart the game?')

                    if clicked == 'OK':
                        self.updateWindow("restart")
                else:
                    displayNoGameRunningMessage()

            # Procedural button clicked
            if event == 'Word':
                if running != 'True':
                    displayNoGameRunningMessage()
                else:
                    self.procedural()

            # Information theory button clicked
            if event == 'Letter':
                if running != 'True':
                    displayNoGameRunningMessage()
                else:
                    self.informationTheory()

            # Random button clicked
            if event == 'Random':
                if running != 'True':
                    displayNoGameRunningMessage()
                else:
                    self.random()

            # Random button clicked
            if event == 'AI':
                if running != 'True':
                    displayNoGameRunningMessage()
                else:
                    self.reinforcementLearning()

class Comparison:

    def __init__(self, clientSocket):
        self.agent = Client(clientSocket)

    def compare(self, listOfAlgorithms, iterations):
        comparisonTable = pd.DataFrame(columns=['phrase','algorithm','win','lives','score','letters_guessed'])
        comparisonFileName = "comparison" + datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + ".csv"
        comparisonTable.to_csv("comparison_data/" + comparisonFileName, index=False)
        difficulty = random.randint(1,3)        # What difficulty the game will be played on. Could be randomly chosen between 1-3
        index = 0
        listOfIntervals = [-1] #[0, 100, 200, 500, 1000, 2000, 4000]
        while index <= iterations:

            self.agent.updateWindow("start game " + str(difficulty))
            gamePhrase = ""

            for algorithm in listOfAlgorithms:

                # Take snapshot of Q-Table at different itervals
                if isinstance(algorithm, QLearning):
                    if index in listOfIntervals:
                        filePath = '.' + algorithm.filePath.strip('.csv') + str(index) + '.csv'
                        algorithm.qTable.to_csv(filePath, index=False)
                        if index != 0:
                            # Adjust algorithm parameters as training progresses
                            algorithm.tuneParameters()
                
                self.agent.runAlgorithm(algorithm)

                updateDetails = phrase.split(":")
                gamePhrase = updateDetails[1].strip()
                win = "Win" in updateDetails[0]
                algorithmName = type(algorithm).__name__

                if algorithmName == 'QLearning':
                    iterationList = re.findall(r'\d+', algorithm.filePath)
                    algorithmName = algorithmName + iterationList[0]
                
                comparisonTable.loc[len(comparisonTable)] = [gamePhrase, algorithmName, win, lives, score, lettersUsed]
                # Append to file
                with open("comparison_data/" + comparisonFileName, mode='a') as file:
                    fileWriter = writer(file)
                    fileWriter.writerow(comparisonTable.iloc[len(comparisonTable) - 1])

                window.read(PAUSE)
                self.agent.updateWindow("restart")

            index += 1      


# Run main() when not imported
if __name__ == "__main__":
    main()
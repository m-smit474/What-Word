# Client.py
# Author: Matthew Smith @m-smit474

import socket
import sys
import PySimpleGUI as sg
import time
from Window import EXIT_BUTTON, window
from Procedural import Procedural
from InformationTheory import InformationTheory

# Standard loopback interface address 127.0.0.1
PORT = 6789 # Port number 

def parseInput(rawInput):
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


def getDifficulty():
    text = None

    
    text = sg.popup_get_text('Enter difficulty between 1-3')

    if text and not(text.isnumeric() and int(text) >= 1 and int(text) <= 3) :
        text = None

    return text


def displayNoServerMessage():
    sg.PopupError("No server found\n",
    "Please try again later or host the server.")

def displayNoGameRunningMessage():
    sg.popup_no_buttons('Start a new game!')


    

def main():

    def updateWindow(command):
        global running
        global phrase
        global guessedLetters

        # Send message to server
        clientSocket.sendall(command.encode())

        # Not guaranteed to read entire message
        inFromServer = clientSocket.recv(1024).decode()
        clientOutput = inFromServer #.lstrip('b')

        update = clientOutput.split("@")[0]
        lives = clientOutput.split("@")[1].split(" ")[0]
        score = clientOutput.split("@")[1].split(" ")[1]
        running = clientOutput.split("@")[1].split(" ")[2]
        guessedLetters = clientOutput.split("@")[1].split(" ", 3)[3].replace("'","")

        if guessedLetters == 'set()':
            guessedLetters = ''

        window["_DISPLAY_"].update(update)
        window["-SCORE-"].update(score)
        window["-LIVES-"].update(lives)
        window["-GUESSED-"].update(guessedLetters)
        window["-GUESS-"].update("")

        phrase = update

    def procedural():
        clicked = sg.popup_ok_cancel('Do you want to run the procedural algorithm?')
    
        if clicked == 'OK':
            runAlgorithm(Procedural())

    def informationTheory():
        clicked = sg.popup_ok_cancel('Do you want to run the information theory algorithm?')
    
        if clicked == 'OK':
            runAlgorithm(InformationTheory())

    def runAlgorithm(algorithm):
        while running == 'True':

            event, values = window.read(2000)

             # End program if user closes window
            if event == "Exit" or event == EXIT_BUTTON:
                break

            guessLetter = algorithm.runAlgorithm(phrase, guessedLetters)
            updateWindow('guess ' + guessLetter)

            


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
                        updateWindow("guess " + str(values['-GUESS-']))
            # New game button clicked
            if event == 'NEW GAME':
                dif = getDifficulty()

                if dif:
                    isRestartable = True
                    updateWindow("start game " + str(dif))


            # Restart button clicked
            if event == 'Restart':
                # You can only restart a game if one has already started
                if isRestartable:
                    clicked = sg.popup_ok_cancel('Do you want to restart the game?')
    
                    if clicked == 'OK':
                        updateWindow("restart")
                else:
                    displayNoGameRunningMessage()

            # Procedural button clicked
            if event == 'Procedural':
                if running != 'True':
                    displayNoGameRunningMessage()
                else:
                    procedural()

            # Information theory button clicked
            if event == 'Info':
                if running != 'True':
                    displayNoGameRunningMessage()
                else:
                    informationTheory()
                
            
        clientSocket.sendall(("exit").encode())
        window.close()

# Run main() when not imported
if __name__ == "__main__":
    main()
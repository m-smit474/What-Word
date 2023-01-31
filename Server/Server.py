# Server.py
# Author: Matthew Smith @m-smit474
import logging
from datetime import datetime
import socket
from threading import *
import Game

HOST = "127.0.0.1" # Standard loopback interface address 127.0.0.1
PORT = 6789 # Port number

class Client(Thread):
    def __init__(self, connection, address):
        # Create thread for client
        Thread.__init__(self) 
        self.sock = connection
        self.addr = address
        self.session = None
        self.start()

    # This method runs the game for a client
    def run(self):
        # with statement using connection will automatically close socket after segment is complete
        with self.sock as connection: 
            print(f"Connected to client {self.addr[1]}")
            logging.debug('Connected to client ' + self.addr[0])

            while True:
                clientInput = connection.recv(1024).decode() # Max read size is 1024

                try:
                    # Create command from input
                    action = Command(clientInput)
                except ValueError as err:
                    # If client send invalid input.
                    # Should only happen if client exits abnormally.
                    print(err.args)
                    break

                action.execute(self)

                if clientInput.lower() == 'exit':
                    break

                if clientInput:
                    if action.command == "end":
                        connection.sendall("Game Ended".encode())
                    elif action.command == "over":
                        self.session.complete = True

                        message = "Out of Lives! Score: " + str(self.session.score) 
                        message += " Phrase: " + self.session.phrase.strip('\n')
                        message = self.addGameDetails(message)
                        connection.sendall(message.encode())
                    elif action.command == "complete":
                        message = "You Win! Score: " + str(self.session.score)
                        message = self.addGameDetails(message)
                        connection.sendall(message.encode())
                    else:
                        # Display hidden phrase
                        message = self.session.hidden 
                        message = self.addGameDetails(message)
                        connection.sendall(message.encode())

            print(f"Client {self.addr[1]} has disconnected")

    def addGameDetails(self, message):
        message += "@"
        message += str(self.session.lives)
        message += " "
        message += str(self.session.score)
        message += " "
        message += str(not self.session.complete)
        message += " "
        message += str(self.session.guessedLetters)

        return message



class Command:
    def __init__(self, rawInput):
        self.phrase = None
        self.letter = None
        self.command= None
        self.difficulty = None
        try:
            self.parse(rawInput)
        except ValueError as err:
            raise ValueError(err.args)


    # Takes user input and returns command
    def parse(self, rawInput):

        tokens = rawInput.split(" ")
        self.command = tokens[0]

        if self.command == "guess":
            if len(tokens[1]) == 1:
                self.letter = tokens[1]
            else:
                i = 1
                self.phrase = ""
                while i < (len(tokens) - 1):
                    self.phrase += tokens[i] + " "
                    i += 1
                self.phrase += tokens[i] + '\n'
        elif self.command == "start" and len(tokens) == 3:
            self.difficulty = tokens[2]
        elif self.command == "exit":
            self.command = "end"
        elif self.command != "end":
            raise ValueError("Could not parse this input: ", rawInput)

    def execute(self, client):
        # TODO
        #global currentSession
        if self.command == "start":
            logging.warning('-----start game-----')
            client.session = Game.Game(self.difficulty)
        elif self.command == "end":
            logging.critical('end')
            logging.warning('-----game over----')    
            client.session = None
        elif self.command == "guess":
            if self.letter:
                logging.info(self.command+":"+self.letter)
                client.session.guessLetter(self.letter)
            elif self.phrase:
                client.session.guessPhrase(self.phrase)
            
            if client.session.isOutOfLives():
                logging.critical('out of lives')
                logging.warning('-----game over----')    
                self.command = "over"
            elif client.session.complete:
                logging.critical('complete')
                logging.warning('-----game over----')    
                self.command = "complete"


def main():
    # Set up logging - One log file for each server run
    logFileName = 'server_log_' + datetime.today().strftime('%Y-%m-%d') + '.log'
    logging.basicConfig(filename="Server/logs/"+logFileName, filemode='w', level=logging.DEBUG)

    # Create a socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind((HOST,PORT))

        # Enables server to accept connections
        serverSocket.listen()
        print("Server started and listening for clients!")
        logging.info('Server Started')


        while True:
            # Blocks execution and waits for incomming connection
            connection, address = serverSocket.accept()

            # Create client object that spawns thread to handle client
            Client(connection, address)

# Run main if not imported
if __name__ == "__main__":
    main()
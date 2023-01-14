import unittest
from Client import parseInput

class TestClient(unittest.TestCase):
    def setUp(self):
        self.errorMessage = ("----------------------------------------\n",
            "Could not process that command.\n",
            "Valid commands are:\n",
            "\tstart game <DIFFICULTY>\n",
            "\tguess <LETTER>\n",
            "\tguess <PHRASE>\n",
            "\tend game\n",
            "\texit\n",
            "----------------------------------------\n")

    def test_parseInput(self):
        #---------------- Valid Input ---------------

        output = parseInput("start game 2")
        self.assertEqual(output, "start game 2")

        output = parseInput("guess l")
        self.assertEqual(output, "guess l")

        output = parseInput("guess word")
        self.assertEqual(output, "guess word")

        output = parseInput("end game")
        self.assertEqual(output, "end game")

        #--------------- Invalid Input ---------------

# Run tests
if __name__ == "__main__":
    unittest.main()
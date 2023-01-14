import unittest
from Game import Game

# A simplified version of a game object
class TestObj():
        def __init__(self):
            self.words = {}
            self.phrase = ""
            self.hidden = ""

class TestGame(unittest.TestCase):

    

    # Runs ONCE before all tests
    """
    def setUpClass(cls):
        pass

    # Runs ONCE after all tests
    def tearDownClass(cls):
        pass
    """

    # Runs before EACH test case
    def setUp(self):
        self.obj = TestObj()
        pass

    # Runs after EACH test case
    def tearDown(self):
        pass

    def test_readWords(self):
        wordCount = 25143
        Game.readWords(self.obj)
        # Check that words is not empty
        self.assertIsNot(self.obj.words, {})
        # Check that there are the correct number of words
        self.assertEqual(len(self.obj.words), wordCount)

    def test_createPhrase(self):
        Game.readWords(self.obj)
        Game.createPhrase(self.obj, 1)
        # Check that phrase is not empty
        self.assertIsNot(self.obj.phrase, "")
        # Check that there are the correct number of words
        Game.createPhrase(self.obj, 1)
        self.assertEqual(len(self.obj.phrase.split(" ")), 1)
        Game.createPhrase(self.obj, 10)
        self.assertEqual(len(self.obj.phrase.split(" ")), 10)

    def test_coverPhrase(self):
        Game.readWords(self.obj)
        Game.createPhrase(self.obj, 1)
        Game.coverPhrase(self.obj)
        allowed = set('_' + ' ')
        # Check that hidden string only contains '_' or ' ' (underscore or space)
        self.assertLessEqual(set(self.obj.hidden), allowed)
        # Check number of hidden words
        self.assertEqual(len(self.obj.hidden.split(" ")), 1)

        # Repeat checks with multiple words
        Game.createPhrase(self.obj, 2)
        Game.coverPhrase(self.obj)
        self.assertLessEqual(set(self.obj.hidden), allowed)
        self.assertEqual(len(self.obj.hidden.split(" ")), 2)

    def test_guessLetter(self):
        game = Game(3)

        # Letter that is likely to be found
        game.guessLetter('e')
        if 'e' in game.phrase:
            self.assertIn('e', game.hidden)
        else:
            self.assertNotIn('e', game.hidden)

        # Letter that is not likely to be found
        game.guessLetter('q')
        if 'q' in game.phrase:
            self.assertIn('q', game.hidden)
        else:
            self.assertNotIn('q', game.hidden)

    def test_guessPhrase(self):
        game = Game(1)
        game.guessPhrase(game.phrase)
        self.assertTrue(game.complete)

        game = Game(1)
        game.guessPhrase("qqqqqqqqq")
        self.assertFalse(game.complete)

        game = Game(10)
        game.guessPhrase(game.phrase)
        self.assertTrue(game.complete)

        game = Game(10)
        game.guessPhrase("q q q q q q q q q q")
        self.assertFalse(game.complete)
    
    def test_score(self):
        #------------- Guess Letter Tests ---------------------
        # guess that will get high score
        game = Game(5)
        game.guessLetter('e')
        letterCount = 0
        points = 0
        for letter in game.phrase:
            if letter == 'e':
                letterCount += 1
                points += (5 * letterCount)

        self.assertEqual(game.score, points)

        # guess that will get low score
        game = Game(1)
        game.guessLetter('q')
        letterCount = 0
        points = 0
        for letter in game.phrase:
            if letter == 'q':
                letterCount += 1
                points += (5 * letterCount)

        self.assertEqual(game.score, points)
        if letterCount == 0:
            self.assertEqual(game.lives, 9)

        #------------- Guess Phrase Tests ---------------------
        game = Game(1)
        game.guessPhrase("q q")
        self.assertEqual(game.lives, 9)
        game.guessPhrase(game.phrase)
        self.assertEqual(game.score, 0)

        game = Game(3)
        game.guessLetter('e')
        score = game.score
        game.guessPhrase(game.phrase)
        self.assertEqual(game.score, (score * game.lives))

        #------------- Out of Lives Tests ----------------------
        game = Game(3)
        game.guessLetter('e')
        thescore = game.score
        for i in range(0,10):
            game.guessLetter('q')
        
        if 'q' not in game.phrase:
            self.assertEqual(game.lives, 0)
            game.isOutOfLives()
            self.assertEqual(game.score, (thescore / 2))







# Run tests
if __name__ == "__main__":
    unittest.main()
# What Word?!
 A client-server game written in Python using socket programming to create TCP connection

In this game, a randomly selected English phrase has all of it's letters replaced with an underscore
character (_) which 'hides' the phrase from the player. The goal of the game is to guess what the
phrase is. This is done by randomly guessing a single letter at a time, hoping the letter is
contained in the phrase. If the letter is in the phrase, all occurrences of the letter will be
'revealed', by replacing the underscore where the letter exists, with the letter itself. The player is
also awarded some points, for each occurance of the letter. If the letter is not found in the word,
the player loses one of ten lives. The game continues with the player guessing letters until the
entire phrase is revealed, or they run out of lives.


# Objective:

The goal of this project is to develop an intelligent agent which is able to play this phrase
guessing game. To begin, we will need a way for the agent to interact with the game, so
developing a process for the agent to play the game will be the first step. Developing an
intelligent agent will be done with 3 different approaches.


1. Procedural Algorithm - (Target Completion Date: Jan 30th, 2023)
This approach will use a relatively simple algorithm which will go through a dictionary of words
to find a good letter to guess. The algorithm will look at what letters have been revealed in the
word, and match those letters and their positions against words in the dictionary narrowing
down potential candidates.
2. Information Theory - (Target Completion Date: Feb 15th, 2023)
The information theory approach is a more sophisticated iteration of the procedural algorithm.
Using a similar methodology to the one described in finding the best wordle opener.¹
We can analyze a data set of words, to derive information that will help us choose a letter to
guess. For example, we can use unsupervised learning to find the frequency of letters in words,
and from that we can see which letters are most likely to appear in a random word.
3. Reinforcement Learning - (Target Completion Date: March 15th, 2023)
The final approach will involve reinforcement learning. In reinforcement learning, an agent
interacts with it's environment taking actions. From those actions, the agent is either rewarded
or punished. There are 3 important characteristics to define for reinforcement learning: State,
Action and Reward. For our situation with the word guessing game we can define state as how
long the current phrase is, what letters are hidden/visible, what letters have already been
guessed. As well as the number of lives remaining and the players score. The only action the
agent will take is guessing a letter. And the reward in our situation would be a letter being
revealed for a correct guess, and points being awarded for guessing correctly.²


# References:
1. Harrison Hoffman. Finding the Best Wordle Opener with Machine Learning [Internet].
[place unknown]: Towards Data Science; February 9, 2022 [updated 2022 February 9;
cited date - 2023 January 3]. Available from:
https://towardsdatascience.com/finding-the-best-wordle-opener-with-machine-learning-c
e81331c5759
2. Géron A. Hands-on Machine Learning with Scikit-Learn, Keras, and TensorFlow :
concepts, tools, and techniques to build intelligent systems. 2nd edition. Sebastopol, CA:
O'Reilly; 2019.
3. Kyriakides G, Margaritis KG. Hands-On Ensemble Learning with Python: Build Highly
Optimized Ensemble Machine Learning Models Using Scikit-Learn and Keras.
Birmingham: Packt Publishing; 2019
4. Mike Ortman. Wikipedia Sentences [data file]. Kaggle: [location unknown]; 2018
[January 3, 2023]. Available from:
https://www.kaggle.com/datasets/mikeortman/wikipedia-sentences
5. Rachael Tatman. English Word Frequency [data file]. Kaggle: [location unknown]; 2017
[January 3, 2023]. Available from:
https://www.kaggle.com/datasets/rtatman/english-word-frequency

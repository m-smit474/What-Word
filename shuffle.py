import random

# Read file
with open("Phrases.txt", "r") as file:
    phrases = []
    for line in file:
        # Skip blank lines
        if len(line) > 1:
            phrases.append(line)

# Shuffle phrases
random.shuffle(phrases)   

# Split data into testing and training sets
train_ratio = 0.8
train_size = int(len(phrases) * train_ratio)

training_data = phrases[0:train_size]
testing_data = phrases[train_size:]

# Write lists to files
with open("data/Phrases_Shuffeled", "w") as writeFile:
    for phrase in phrases:
        writeFile.write(f"{phrase}\n")

with open("data/training_data.txt", "w") as writeFile:
    for phrase in training_data:
        writeFile.write(f"{phrase}\n")

with open("data/testing_data.txt", "w") as writeFile:
    for phrase in testing_data:
        writeFile.write(f"{phrase}\n")
import pandas as pd

wordFrequencyDataFrame = pd.read_csv("English_Word_Frequency/unigram_freq.csv")

print(wordFrequencyDataFrame.head())

wordFrequencyDataFrame["word_length"] = 0

wordFrequencyDataFrame.reset_index()
index = 0
for row in wordFrequencyDataFrame.iterrows():
    if not isinstance(row[1]['word'], float):
        wordFrequencyDataFrame.iloc[[index], [2]] = len(row[1]['word'])
    index = index + 1
    if index % 50000 == 0:
        print(str(index/333333) + '%')

print(wordFrequencyDataFrame.head())

wordFrequencyDataFrame.to_csv("English_Word_Frequency/word_frequency.csv", index=False)
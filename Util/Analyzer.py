import pandas as pd
import matplotlib.pyplot as plt
import sys
import os.path

class Analyzer:
    def __init__(self):
        filePath = input('Enter data file path (Example: comparison_data/comparison.csv) \n')
        if os.path.isfile(filePath):
            self.comparisonDataFrame = pd.read_csv(filePath)
        else:
            print("Failed to find file")
            sys.exit(1)

    def calculateWinRate(self):

        winRateData = {}
        for row in self.comparisonDataFrame.iterrows():
            algorithm = row[1]["algorithm"]

            if algorithm not in winRateData:
                winRateData.update({algorithm:[]})
            
            listOfWins = winRateData.get(algorithm)
            listOfWins.append(int(row[1]["win"]))
            winRateData.update({algorithm:listOfWins})


        winRateDataFrame = pd.DataFrame(winRateData)

        winPercentage = winRateDataFrame.mean(axis=0)
        print("\nWin Rates:")
        print(winPercentage)
        winPercentage.plot(kind="bar")
        plt.show()


if len(sys.argv) == 2 and sys.argv[1] == 'winrate':
    analyzer = Analyzer()
    analyzer.calculateWinRate()
elif len(sys.argv) == 3 and sys.argv[1] == 'qtable' and sys.argv[2].isnumeric:
    iterations = str(sys.argv[2])
    fileName = 'QTable_Data/QTable' + iterations + '.csv'
    try:
        qTableDataFrame = pd.read_csv(fileName)
        start = qTableDataFrame.iloc[0]
        correct = qTableDataFrame.iloc[1]
        incorrect = qTableDataFrame.iloc[2]
        graphTitle = "Qtable " + iterations + " Iterations"
        qTableDataFrame.mean(axis=0).plot(kind="bar", title=graphTitle)
        plt.show()
    except FileNotFoundError:
        print("Could not open file " + fileName)
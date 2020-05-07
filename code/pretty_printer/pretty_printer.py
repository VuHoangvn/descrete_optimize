import sys

class PrettyPrinter():
    def __init__(self, inFile, lineLength):
        self._inFile = inFile
        self._lineLength = lineLength
        self._text = []

    def readInput(self):
        with open(self._inFile, 'r') as f:
            for line in f.readlines():
                self._text.append(line)

    def writeOutput(self):
        for line in self._text:
            print(line)
    
    def pretty(self):
        output = ''
        for para in self._text:
            words = para.split()
            if words == []:
                output += "\n"
                continue
            output += Utils.justify(words, self._lineLength)
            print(output)

class Utils:
    @classmethod
    def justify(cls, words, lineLength):
        cost = [[0 for _ in range(len(words))] for _ in range(len(words))]


        # next 2 for loop is used to calculate cost of putting words from 
        # i to j in one line. If words don't fit in one line then we put
        # sys.maxsize
        for i in range(len(words)):
            cost[i][i] = lineLength - len(words[i])
            for j in range(i+1, len(words)):
                cost[i][j] = cost[i][j-1] - len(words[j]) + 1

        for i in range(len(words)):
            for j in range(i, len(words)):
                if cost[i][j] < 0:
                    cost[i][j] = sys.maxsize
                else:
                    cost[i][j] = int(pow(cost[i][j], 2))

        # minCost from i to len is found by trying
        # j between i to len and checking which 
        # one has min value
        minCost = [0 for _ in range(len(words))]
        result = [0 for _ in range(len(words))]
        for i in range(len(words)-1, -1, -1):
            minCost[i] = cost[i][len(words)-1]
            result[i] = len(words)
            for j in range(len(words)-1, i, -1):
                if cost[i][j-1] == sys.maxsize:
                    continue
                if minCost[i] > minCost[j] + cost[i][j-1]:
                    minCost[i] = minCost[j] + cost[i][j-1]
                    result[i] = j

        i = 0
        j = result[0]
        output = ''

        while(j < len(words)):
            for k in range(i, j):
                output += words[k] + " "
            output += "\n"
            i = j
            j = result[i]

        return output



if __name__ == '__main__':
    if len(sys.argv) > 2:
        inputFile = sys.argv[1].strip()
        # try:
        lineLength = int(sys.argv[2].strip())
        pp = PrettyPrinter(inputFile, lineLength)
        pp.readInput()
        pp.pretty()
            # pp.writeOutput()
        # except:
        #     print("Line length must be an integer number. (i.e. 80)")
    
    else:
        print('This test requires an input file and a number. Please selece one from the data directory and one number.')
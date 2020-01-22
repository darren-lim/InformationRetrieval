import os
import re
import string
import sys
# Darren Lim 24233004
# please run in python 3

'''
Tokenize has a time complexity dependent on the size of the text file. O(N)
'''
def tokenize(TextFilePath):
    if os.stat(TextFilePath).st_size == 0:
        print(TextFilePath + " is Empty")
        return []
    file = open(TextFilePath, "r")
    tokenList = []
    for line in file:
        line = re.sub(r'[^\x00-\x7f]', r' ', line).lower()
        line = line.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
        tokenList.extend(line.split())
    if len(tokenList) == 0:
        print("No valid tokens in the " + TextFilePath + " file.")
    return tokenList

'''
computeWordFrequencies has a time complexity dependent on the size of the input. O(N)
'''
def computeWordFrequencies(ListOfToken):
    wordFreqDict = {}
    for token in ListOfToken:
        if token not in wordFreqDict:
            wordFreqDict[token] = 1
        else:
            wordFreqDict[token] += 1
    return wordFreqDict


'''
printFreq has a time complexity dependent on the size of the input.
The function sorts the frequency dictionary, thus the complexity is O(n log n)
'''
def printFreq(Frequencies):
    sortedFreq = sorted(Frequencies.items(), key = lambda val: val[1], reverse=True)
    for item in sortedFreq:
        print(str(item[0]) + " -> " + str(item[1]))

'''
main function
'''
if __name__ == '__main__':
    if(len(sys.argv)>2):
        print("More than one text file inputted, will parse through all.")
    for i in sys.argv[1:]:
        if not os.path.exists(i):
            print("Path of file is Invalid")
            continue
        tlist = tokenize(i)
        freqDict = computeWordFrequencies(tlist)
        printFreq(freqDict)
        print()

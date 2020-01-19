import os
import re
import string
# Darren Lim 24233004

def test():
    while(True):
        uInput = input("Enter File Path: ")
        if not os.path.exists(uInput):
            print("Path of file is Invalid")
            continue
        elif os.stat(uInput).st_size == 0:
            print("File is Empty")
            continue
        break
    tlist = tokenize(uInput)
    print(tlist)
    freqDict = computeWordFrequencies(tlist)
    printFreq(freqDict)

'''
Param:  valid text file path
Return: A list of tokenized words in the file
Description: Tokenize takes a file path, reads the lines, removes non english characters,
                makes all characters lowercase, and splits the lines into a list. The
                method also includes punctuation because they are characters, but exclude
                spaces.
'''
def tokenize(TextFilePath):
    file = open(TextFilePath, "r")
    tokenList = []
    for line in file:
        line = re.sub(r'[^\x00-\x7f]', r' ', line).lower()
        line = line.translate(str.maketrans('', '', string.punctuation))
        tokenList.extend(line.split())
    if len(tokenList) == 0:
        print("No valid tokens in the text file.")
    return tokenList


def computeWordFrequencies(ListOfToken):
    wordFreqDict = {}
    for token in ListOfToken:
        if token not in wordFreqDict:
            wordFreqDict[token] = 1
        else:
            wordFreqDict[token] += 1
    return wordFreqDict

def printFreq(Frequencies):
    sortedFreq = sorted(Frequencies.items(), key = lambda val: val[1], reverse=True)
    for item in sortedFreq:
        print(str(item[0]) + " -> " + str(item[1]))

if __name__ == '__main__':
    test()
import os
import string
import re
import sys
#Darren Lim 24233004

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
        line = line.translate(str.maketrans('', '', string.punctuation))
        tokenList.extend(line.split())
    if len(tokenList) == 0:
        print("No valid tokens in the " + TextFilePath + " file.")
    return tokenList

'''
compareTokens has a complexity of O(N+M), where n is the first input and m is the second.
This is because we turn both lists into a set, then iterate over the SMALLER set while checking
if the word exists in the larger set.
'''
def compareTokens(listA, listB):
    #setIntersect = {}
    if(len(listA) <= len(listB)):
        setIntersect = frozenset(listA).intersection(listB)
    else:
        setIntersect = frozenset(listB).intersection(listA)
    return setIntersect

def printComparisons(setInput):
    print(len(setInput))
    for i in setInput:
        print(i)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        sys.exit("Too many arguments.")
    elif len(sys.argv) < 3:
        sys.exit("Need 2 text files.")

    text1 = sys.argv[1]
    text2 = sys.argv[2]
    if not os.path.exists(text1):
        sys.exit("Path " + text1 + " is Invalid")
    if not os.path.exists(text2):
        sys.exit("Path " + text2 + " is Invalid")

    tlist1= tokenize(text1)
    tlist2 = tokenize(text2)
    tokenSet = compareTokens(tlist1, tlist2)
    printComparisons(tokenSet)

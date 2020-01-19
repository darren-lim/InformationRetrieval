import os
import string
import re

def test():
    while(True):
        uInput = input("Enter File Path: ")
        if not os.path.exists(uInput):
            print("Path of file is Invalid")
            continue
        elif os.stat(uInput).st_size == 0:
            print("File is Empty")
            continue
        uInput2 = input("Enter File Path 2: ")
        if not os.path.exists(uInput2):
            print("Path of file is Invalid")
            continue
        elif os.stat(uInput2).st_size == 0:
            print("File is Empty")
            continue
        break
    tlist1= tokenize(uInput)
    tlist2 = tokenize(uInput2)
    compareTokens(tlist1, tlist2)

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

def compareTokens(listA, listB):
    #setIntersect = {}
    if(len(listA) <= len(listB)):
        setIntersect = frozenset(listA).intersection(listB)
    else:
        setIntersect = frozenset(listB).intersection(listA)
    print(len(setIntersect))
    for i in setIntersect:
        print(i)

if __name__ == '__main__':
    test()
import os

# Darren Lim 24233004

def test():
    while(True):
        uInput = input("Enter File Path: ")
        if not os.path.exists(uInput):
            print("Path of file is Invalid")
            continue
        break
    file = open(uInput, "r")
    for line in file:
        print(line)

def tokenize(TextFilePath):
    pass

def computeWordFrequencies(ListOfToken):
    pass

def printFreq(Frequencies):
    pass

if __name__ == '__main__':
    test()
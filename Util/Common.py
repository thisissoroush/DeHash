from . import DB
import json
import string
import itertools
import hashlib
import time
import os

ConnectionString = None
lstChar = []


def DoHashGuess(latestCharToHash,requestedHash):
    global lstChar

    latestExists = True
    if(latestCharToHash in (None,"")):
        latestCharToHash = lstChar[0]
        latestExists = False
    try:
        strLength = len(latestCharToHash)
        latestChar = latestCharToHash[-1]
        print("Starting with {0} word with length of {1} and the last char with {2}".format(
            latestCharToHash.replace(' ',"(Space)"),strLength,latestChar))
        ix = 0

        while(True):
            start_time = time.time()

            possibleWords = DB.GetPossibleWords(len(latestCharToHash))
            if(len(possibleWords) == 0):
                print("no guess already")
                raise Exception('sleeping 1 hr!')
            print('Possible words with length of {0} are {1}'.format(
                str(strLength),str(len(possibleWords))))
            
            if(latestExists):
                ix = possibleWords.index(latestCharToHash) + 1
                print('latest char founded')

            for i in range(len(possibleWords) - ix):
                currentWord = possibleWords[i + ix]
                hashed = HashPassword(currentWord)
                DB.InsertHashData(currentWord,hashed)
                # print('hasheed data of {0} set.'.format(currentWord))
                if(requestedHash not in (None,"") and hashed == requestedHash):
                    print("Requested hash Founded, move to the next one")
                    DB.RemoveRequestedHash(requestedHash)
                    requestedHash = DB.GetRequestedHash()

            strLength += 1
            ix = 0
            latestExists = False
            print("Guess Hash with length of {0} completed after {1} minutes.".format(
                strLength - 1,round((time.time() - start_time) / 60.0,2)
            ))

    except Exception as e:
        print(str(e))
        raise Exception('sleeping 1 hr!')

def GuessWords(length):
    global lstChar

    possibleWords = list(PossibleCombinations(length,lstChar))
    possibleWords = [''.join(i) for i in possibleWords]
    DB.InsertPossibleWords(possibleWords)

def PossibleCombinations(length,lst):
    yield from itertools.product(*([lst] * length))

def HashPassword(pwrd):
    pwrd = pwrd.encode("UTF-8")
    password = hashlib.sha256()
    password.update(pwrd)
    return password.hexdigest()

def SplitString(word):
    return [char for char in word]

def SetStartupValues():
   
    global ConnectionString
    global lstChar

    lstChar = SplitString(string.printable)[:95]

    with open('config.json') as json_file:
        config = json.load(json_file)
        ConnectionString = config["ConnectionString"]
        
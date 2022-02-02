from Util import Common,DB
import time

requestedHash = None
latestCharToHash = None

if __name__ == "__main__":
    
    while(True):
        try:
            Common.SetStartupValues()
            for i in range(15):
                if( i <= 2):
                    continue
                startTime = time.time()
                print("Start Guessing for length of " + str(i))
                Common.GuessWords(i)
                print("Guess Hash with length of {0} completed after {1} minutes.".format(
                str(i),round((time.time() - startTime) / 60.0,2)
            ))
        except:
            pass


from Util import Common,DB
import time


requestedHash = None
latestCharToHash = None


if __name__ == "__main__":
    
    while(True):
        try:
            Common.SetStartupValues()
            latestCharToHash = DB.GetLatestString()
            requestedHash = DB.GetRequestedHash()
            if(requestedHash not in (None,"")):
                print("Requested Hash fetched")
            Common.DoHashGuess(latestCharToHash,requestedHash)
        except:
            time.sleep(3600)
            pass


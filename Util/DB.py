from typing import Counter
from . import Common
import pyodbc
from datetime import datetime
import time


def GetRequestedHash():
    res = None
    try:
        if(Common.ConnectionString != ""):
            query = "SELECT TOP 1 Hashed FROM RequestedHashStrings"
            conn = pyodbc.connect(Common.ConnectionString)
            cursor = conn.cursor()
            cursor.execute(query) 
            rows = cursor.fetchall()
            
            if( len(rows)>0):
                res = rows[0][0]

            conn.commit()
            conn.close()
    except:
        pass
    finally:
        return res

def RemoveRequestedHash(hash):
    try:
        if(Common.ConnectionString != ""):
            query = "DELETE FROM RequestedHashStrings WHERE Hashed=N'{0}'".format(hash)
            conn = pyodbc.connect(Common.ConnectionString)
            cursor = conn.cursor()
            cursor.execute(query) 
            conn.commit()
            conn.close()
    except:
        pass

def GetLatestString():
    res = None
    try:
        if(Common.ConnectionString != ""):
            query = "SELECT TOP 1 NonHashedString FROM hashedstrings ORDER BY Id DESC"
            conn = pyodbc.connect(Common.ConnectionString)
            cursor = conn.cursor()
            cursor.execute(query) 
            rows = cursor.fetchall()
            
            if( len(rows)>0):
                res = rows[0][0]

            conn.commit()
            conn.close()
    except:
        pass
    finally:
        return res

def InsertHashData(word,hash):
    try:
        if(Common.ConnectionString != ""):
            query = "INSERT hashedstrings VALUES(N'{0}',N'{1}')".format(word,hash)
            conn = pyodbc.connect(Common.ConnectionString)
            cursor = conn.cursor()
            cursor.execute(query) 
            conn.commit()
            conn.close()
    except:
        pass


def InsertPossibleWords(words):
    mainquery = "INSERT PossibleWords VALUES "
    tmp = ""
    for i in range(len(words)):
        try:
            word = words[i]
            tmp += "(N'{0}',{1}),".format(word.replace("'","''"),len(word))
            if( (i > 0 and i%90 == 0) or i == len(words) - 1):
                if(Common.ConnectionString != ""):
                    query = mainquery + tmp[:-1:]
                    conn = pyodbc.connect(Common.ConnectionString)
                    cursor = conn.cursor()
                    cursor.execute(query) 
                    conn.commit()
                    conn.close()
                    tmp = ""
        except:
            pass

def GetPossibleWords(length):
    res = []
    try:
        if(Common.ConnectionString != ""):
            counter = 0
            while(True):
                startTime = time.time()
                query = """ SELECT Word 
                            FROM PossibleWords 
                            WHERE [length] = {0} 
                            ORDER BY Word   
                            OFFSET {1} ROWS 
                            FETCH NEXT 10000000 ROWS ONLY""".format(str(length),str(10000000*counter))
                counter += 1
                conn = pyodbc.connect(Common.ConnectionString)
                cursor = conn.cursor()
                cursor.execute(query) 
                rows = cursor.fetchall()
                conn.commit()
                conn.close()
                print("fetched 10M rows on round {0} in {1} seconds.".format(str(counter),round((time.time() - startTime),2)))
                if( len(rows)>0):
                    res.extend([x[0] for x in rows])
                else:
                    break
            
    except:
        pass
    finally:
        return res
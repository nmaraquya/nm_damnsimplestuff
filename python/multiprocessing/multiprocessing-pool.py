#python 3.x
from multiprocessing import Pool
import os
import time

def squareIT(n):
    return n**2

def squareNumber(ns):
    result=[]
    for i in(ns):
        result.append(i**2)
    return result

# function to be mapped over
def calculateParallelLISTS(lists, threads=2):
    pool = Pool(threads)
    results = pool.map(squareNumber, lists)
    pool.close()
    pool.join()
    return results

def calculateParallel(listIK, threads=2):
    pool = Pool(threads)
    results = pool.map(squareIT, listIK)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":

    startedAt = time.time()
    sublistdepth=250000
    listoflists=[]
    tmplist=[]
    for i in range(10000000):
        tmplist.append(i)
        if len(tmplist)>=sublistdepth:
            listoflists.append(tmplist)
            tmplist=[]
    
    print("formed list of lists of numbers in "+str(round(time.time()-startedAt,2))+" secs")
    startedAt = time.time()


    tmplist=[]
    for i in range(10000000):
        tmplist.append(i)
    print("formed list of numbers in "+str(round(time.time()-startedAt,2))+" secs")

    
    startedAt = time.time()
    pool_output = calculateParallel(tmplist,1)
    print("1 thread done task in "+str(round(time.time()-startedAt,2))+" secs")


    startedAt = time.time()
    pool_output = calculateParallel(tmplist,4)
    print("4 thread done task in "+str(round(time.time()-startedAt,2))+" secs")

    
    startedAt = time.time()
    pool_output = calculateParallelLISTS(listoflists,1)
    print("1 thread done task in "+str(round(time.time()-startedAt,2))+" secs")


    startedAt = time.time()
    pool_output = calculateParallelLISTS(listoflists,4)
    print("4 thread done task in "+str(round(time.time()-startedAt,2))+" secs")
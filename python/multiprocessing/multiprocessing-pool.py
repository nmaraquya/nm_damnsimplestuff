#python 3.x
from multiprocessing import Pool
import os
import time

def squareIT(n):
    return n**2


def calculateParallel(listIK, threads=2):
    pool = Pool(threads)
    results = pool.map(squareIT, listIK)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":

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

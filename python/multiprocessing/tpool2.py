from multiprocessing.dummy import Pool as ThreadPool
import time 


def sleepsecs(n):
    time.sleep(n)

# function to be mapped over
def sleepParallel(numbers, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(sleepsecs, numbers)
    pool.close()
    pool.join()
    return results

numbers = [1, 2, 3, 4, 5]
squaredNumbers = sleepParallel(numbers, 4)

print("1 thread done task in "+str(round(time.time()-startedAt,2))+" secs")
from multiprocessing.dummy import Pool as ThreadPool
import time 


startedAt = time.time()
def squareNumber(n):
    time.sleep(1)

# function to be mapped over
def calculateParallel(numbers, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(squareNumber, numbers)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
    
    numbers = [1, 2, 3, 4, 5,6,7,8,9,10]
    squaredNumbers = calculateParallel(numbers, 8)

print(round(time.time()-startedAt,2))
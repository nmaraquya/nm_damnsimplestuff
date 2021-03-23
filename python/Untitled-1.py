#!/usr/bin/env python3

# assing 10 jobs hello() to 10 threads and print "Done!"

import threading
import time
import random

def hello(n):
    sleeptime = round(random.randint(0,3000000)/10000000,1)
    time.sleep(sleeptime)
    print("Thread # [{0}] says Hello!, was asleep [{1}] seconds.".format(n,sleeptime))

for i in range(10): 
    print("Assign job hello() to Thread [{0}]".format(i))
    print("Threads ALIVE: " + str(len(threading.enumerate())))
    threading.Thread(target=hello, args=(i,)).start()

# their not blocks main thread 
# each thread will killed after end of target function

print("All jobs assigned!")
print("Threads ALIVE: " + str(len(threading.enumerate())))
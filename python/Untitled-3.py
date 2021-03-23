#!/usr/bin/env python3

import multiprocessing
import time
import random

def hello(n):
    sleeptime = round(random.randint(0,3000000)/10000000,3)
    time.sleep(sleeptime)
    print("Process # [{0}] says Hello!, was asleep [{1}] seconds.".format(n,sleeptime))

processes = [ ]
for i in range(10):
    t = multiprocessing.Process(target=hello, args=(i,))
    processes.append(t)
    print("Assign job hello() to process [{0}]".format(i))
    t.start()

for one_process in processes:
    print(".join() Process "+str(one_process))
    one_process.join()

print("Done!")
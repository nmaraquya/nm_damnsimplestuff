
#!/usr/bin/env python3

# sharing data between process using fifo queue

import multiprocessing
import time
import random
import os
from multiprocessing import Queue

q = Queue()

def hello(n):
    sleeptime = round(random.randint(0,3000000)/10000000,1)
    time.sleep(sleeptime)
    q.put(os.getpid())
    print("Process # [{0}] says Hello!, was asleep [{1}] seconds.".format(n,sleeptime))

processes = [ ]
for i in range(10):
    t = multiprocessing.Process(target=hello, args=(i,))
    processes.append(t)
    t.start()

for one_process in processes:
    one_process.join()

mylist = [ ]
while not q.empty():
    mylist.append(q.get())

print("Done!")
print(len(mylist))
print(mylist)
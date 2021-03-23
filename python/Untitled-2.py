#!/usr/bin/env python3

import threading
import time
import random

def hello(n):
    sleeptime = round(random.randint(0,3000000)/10000000,3)
    time.sleep(sleeptime)
    print("Thread # [{0}] says Hello!, was asleep [{1}] seconds.".format(n,sleeptime))

threads = [ ]
for i in range(10):
    t = threading.Thread(target=hello, args=(i,))
    threads.append(t)
    print("Assign job hello() to Thread [{0}]".format(i))
    print("Threads ALIVE: " + str(len(threading.enumerate())))
    t.start()

# .join() method blocks main thread until this tread would not be killed

for one_thread in threads:
    print(".join() thread "+str(one_thread))
    one_thread.join()

print("Done!")
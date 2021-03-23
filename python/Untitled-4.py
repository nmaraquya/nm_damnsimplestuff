#!/usr/bin/env python3

# share global variable "mylist" with all threads

import threading
import time
import random

mylist = [ ]

def hello(n):
    sleeptime = round(random.randint(0,3000000)/10000000,1)
    time.sleep(sleeptime)
    mylist.append(threading.get_ident())   # bad in real code!
    print("Thread # [{0}] says Hello!, was asleep [{1}] seconds.".format(n,sleeptime))

threads = [ ]
for i in range(10):
    t = threading.Thread(target=hello, args=(i,))
    threads.append(t)
    print("Assign job hello() to Thread [{0}]".format(i))
    t.start()

for one_thread in threads:
    print(".join() Thread "+str(one_thread))
    one_thread.join()

print("Done!")
print(len(mylist))
print(mylist)
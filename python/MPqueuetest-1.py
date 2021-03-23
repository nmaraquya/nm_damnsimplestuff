#!/usr/bin/env python3

"""
dummy multiprocess programm
! it is possible to use multiprocess and queues as interprocess communications for UDP based data transmission in python
"""

import multiprocessing
import time
import random
import os
import sys

pkts = 8600

qu = multiprocessing.Queue()

# packets for 100Mbps 8514.986376021798
# IPIS: 0.00011744000000000001 seconds



def senderProcess():
    print("Hello from sender")
    i=0
    sendlen=0
    start = time.time()
    while i < pkts:
        i+=1
        pkt = os.urandom(1500)
        sendlen+=sys.getsizeof(pkt)
        qu.put(pkt)
        print("send qsize: "+str(qu.qsize()))
    print("Sender spent time: "+str(time.time()-start)+"; sendrate: "+str((8*sendlen / (time.time()-start)/1e6))+" Mbps; IPIS = "+str(1/(pkts / (time.time()-start))))
    print("Got "+str(sendlen/1048576)+" MBytes; Goodbye from sender")

def receiverProcess():
    print("Hello from receiver")
    i=0
    recvlen=0
    start = time.time()
    while i < pkts:
        i+=1
        pkt = qu.get()
        recvlen+=sys.getsizeof(pkt)
        print("recv qsize: "+str(qu.qsize()))
    print("Receiver spent time: "+str(time.time()-start)+"; recvrate: "+str((8*recvlen / (time.time()-start)/1e6))+" Mbps; IPIR = "+str(1/(pkts / (time.time()-start))))
    print("Got "+str(recvlen/1048576)+" MBytes; Goodbye from receiver")


sender = multiprocessing.Process(target=senderProcess, args=())
receiver = multiprocessing.Process(target=receiverProcess, args=())
receiver.start()
sender.start()
sender.join()
receiver.join()
print("finish")

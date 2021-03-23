import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

# difference between daemon and non-daemon threads:
# daemon thread can be killed at the end of the main thread before end of damon thread
# non-daemon thread would make main thread to wait until non-daemon threads would end before exit() on main thread

def n():
    logging.debug('Starting')
    time.sleep(2)
    logging.debug('Exiting')

def d():
    logging.debug('Starting')
    time.sleep(5)
    logging.debug('Exiting')

if __name__ == '__main__':

	t = threading.Thread(name='non-daemon', target=n)

	d = threading.Thread(name='daemon', target=d)
	d.setDaemon(True)

	d.start()
	t.start()
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

# use .join() to wait until daemon thread would be ended

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

	d.join()
	t.join()
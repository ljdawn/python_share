#! /usr/bin/env python
"""
# Consume one item
cv.acquire()
while not an_item_is_available():
        cv.wait()
        get_an_available_item()
        cv.release()

# Produce one item
cv.acquire()
make_an_item_available()
cv.notify()
cv.release()
"""

import threading
import time

class Test(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self._run_num = num

    def run(self):
        global count, mutex
        threadname = threading.currentThread().getName()

        for x in xrange(0, int(self._run_num)):
            mutex.acquire()
            count += 1
            mutex.release()
            print threadname, x, count
            time.sleep(1)

if __name__ == "__main__":
    global count, mutex
    threads = []
    num = 4
    count = 1
    mutex = threading.Lock()
    # create threads
    for x in xrange(0, num):
        threads.append(Test(10))
    # start threads
    for t in threads:
        t.start()
    # wait for  threads ending
    for t in threads:
        t.join()

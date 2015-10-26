#! /usr/bin/env python
# encoding:utf-8

from socket import *
from threading import Thread
from Queue import Queue
 
def scan(ip,port):
    s=socket(AF_INET,SOCK_STREAM)
    result=s.connect_ex((ip,port))
    if(result==0):
        print 'Port %d: OPEN' % port
    s.close()
 
class Worker(Thread):
    def __init__(self,taskQueue):
        Thread.__init__(self)
        self.setDaemon(True)
        self.taskQueue=taskQueue
        self.start()
 
    def run(self):
        while True:
            try:
                callable,args,kwds=self.taskQueue.get(block=False)
                callable(*args,**kwds)
            except:
                break
 
class ThreadPool:
    def __init__(self,ip):
        self.threads=[]
        self.taskQueue=Queue()
        self.threadNum=10
        self.__create_taskqueue(ip)
        self.__create_threadpool(self.threadNum)
 
    def __create_taskqueue(self,ip):
        for i in range(20,10000):
            self.add_task(scan,ip,i)
 
    def __create_threadpool(self,threadNum):
        for i in range(threadNum):
            thread=Worker(self.taskQueue)
            self.threads.append(thread)
 
    def add_task(self,callable,*args,**kwds):
        self.taskQueue.put((callable,args,kwds))
 
    def waitfor_complete(self):
        while len(self.threads):
            thread=self.threads.pop()
            thread.join()
            if thread.isAlive() and not self.taskQueue.empty():
                self.threads.append(thread)
        print 'scaning is over!'
 
if __name__=='__main__':
    target=raw_input('Enter host to scan:')
    targetIP=gethostbyname(target)
    print 'Starting scan on host',targetIP
    tp=ThreadPool(targetIP)
    tp.waitfor_complete()

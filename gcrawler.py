# -*- coding: utf-8 -*-

'''
    gevent crawler
    ~~~~~~~~~~~~~~~~
    BSD License
    2011 by raptor.zh@gmail.com.
'''

import gevent
from gevent import monkey, queue

monkey.patch_all()

import urllib2
from time import sleep
import traceback
import logging

logger = logging.getLogger(__name__)

class GCrawler:
    def __init__(self, spider, timeout=5, workers_count=8, pipeline_size=100):
        self.spider = spider
        self.timeout = timeout
        self.qin = queue.Queue(0)
        self.qout = queue.Queue(pipeline_size)
        self.jobs = [gevent.spawn(self.doScheduler)]
        self.jobs += [gevent.spawn(self.doWorker) for i in range(workers_count)]
        self.jobs += [gevent.spawn(self.doPipeline)]
        self.job_count = len(self.jobs)

    def start(self):
        gevent.joinall(self.jobs)

    def doScheduler(self):
        try:
            scheduler = self.spider.scheduler()  #  return a generator
            for item in scheduler:
                self.qin.put(item)
        except Exception, e:
            logger.error("Scheduler Error!\n%s" % traceback.format_exc())
        finally:
            for i in range(self.job_count - 2):
                self.qin.put(StopIteration)
            self.job_count -= 1
            logger.debug("Scheduler done, job count: %s" % self.job_count)

    def doWorker(self):
        try:
            item = self.qin.get()
            while item != StopIteration:
                try:
                    r = self.spider.worker(item)
                    if r != None:
                        self.qout.put(r)
                except:
                    logger.error("Worker error!\n%s" % traceback.format_exc())
                item = self.qin.get()
        finally:
            self.job_count -= 1
            logger.debug("Worker done, job count: %s" % self.job_count)

    def doPipeline(self):
        while self.job_count > 1 or not self.qout.empty():
            sleep(self.timeout)
            try:
                results = []
                try:
                    while True:
                        results.append(self.qout.get_nowait())
                except queue.Empty:
                    if results != []:
                        self.spider.pipeline(results)
            except:
                logger.error("Pipeline error!\n%s" % traceback.format_exc()) 

def retryOnURLError(trycnt=3):
    def funcwrapper(fn):
        def wrapper(self, *args, **kwargs):
            for i in range(trycnt):
                try:
                    return fn(self, *args, **kwargs)
                except urllib2.URLError, e:
                    logger.info("retry %s time(s)" % (i+1))
                    if i == trycnt - 1:
                        raise e
        return wrapper
    return funcwrapper

class Downloader:
    def __init__(self, urls):
        self.urls = urls
        self.subitems = queue.Queue(-1)
        self.parsings = 0

    def scheduler(self):
        parse=None
        if hasattr(self, 'parse'):
            parse = self.parse
        for u in self.urls:
            if parse != None:
                self.parsings += 1
            yield dict(url=u, parse=parse)
        while self.parsings > 0:
            sleep(1)
            while not self.subitems.empty():
                item = self.subitems.get()
                try:
                    if item['parse'] != None:
                        self.parsings += 1
                except:
                    pass
                yield item

    def worker(self, item):
        r = None
        try:
            r = self.doWorker(item['url'])
            if r != None and item['parse'] != None:
                try:
                    new_items, r = item['parse'](r)
                    for i in new_items:
                        self.subitems.put(i)
                finally:
                    self.parsings -= 1
        except Exception, e:
            logger.error("Error on get %s:%s\n%s" % (item['url'], e, traceback.format_exc()))
        return r

    @retryOnURLError(3)
    def doWorker(self, url):
        logger.debug("Download starting...%s" % url)
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()
        return dict(url=url, data=data)



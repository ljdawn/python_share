#! /usr/bin/env python

import os
import time
import threading
import requests
from Queue import Queue
from lxml import html


base = os.path.expanduser("~/data/biquge")
root = "http://www.biquge.la"
start_urls = ["http://www.biquge.la/xuanhuanxiaoshuo/",
             "http://www.biquge.la/xiuzhenxiaoshuo/",
             "http://www.biquge.la/dushixiaoshuo/",
             "http://www.biquge.la/lishixiaoshuo/",
             "http://www.biquge.la/wangyouxiaoshuo/",
             "http://www.biquge.la/kehuanxiaoshuo/",
             ]

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://cl.loius.biz/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
           }


class GetContent(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self)
        self.name = t_name
        self.queue = queue
    def run(self):
        while True:
            if not self.queue.empty():
                queueLock.acquire()
                _path, url = self.queue.get()
                print "threading name: %s"%self.name, url
                queueLock.release()
                fl = os.path.join(_path, url.split('/')[-1])
                with open(fl, "w") as file:
                    print "writing file %s"%fl
                    req = requests.session()
                    resp = req.get(url, headers = headers)
                    content = resp.content.decode('gbk', 'ignore').encode('utf8', 'ignore')
                    file.write(content)
            else:
                time.sleep(60)
                if self.queue.empty():
                    break
    def stop(self):  
        self.thread_stop = True  
                

def get_page(url):
    print "processing %s"%url
    req = requests.session()
    resp = req.get(url, headers = headers)
    get_book_list(resp.url, resp.content.decode("gbk"))

def get_book_list(prev_url, page):
    """
    page is just the content from requests.
    xpaths:span[@class="s2"]/a
    """
    print "processing %s"%prev_url
    page = html.fromstring(page)
    #urls = page.xpath("//div[@class='l']/span[@class='s2']/a['href']")
    urls = page.xpath("//div[@class='l']//span[@class='s2']/a['href']")
    type_path = os.path.join(base,prev_url.split('/')[-2])
    urls = (root+url.values()[0] for url in urls)
    for url in urls:
        book_path = os.path.join(type_path, url.split('/')[-2])
        if not os.path.exists(book_path):
            os.makedirs(book_path)
        get_section_list(book_path, url)

def get_section_list(_path, url):
    """
    dd/a
    page is just the content from requests.
    """
    print "processing %s"%url
    req = requests.session()
    resp = req.get(url) 
    page = html.fromstring(resp.content.decode("gbk", "ignore"))
    urls = page.xpath("//dd/a['href']")
    #urls = (url+_url.values()[0] for _url in urls)
    for _url in urls:
        cur_url =  url+_url.values()[0]
        queue.put([_path, cur_url])

queue = Queue()
queueLock = threading.Lock()

threads = []
for url in start_urls:
    t = threading.Thread(target=get_page,args=(url,))
    threads.append(t)

for i in range(10):
    thread = GetContent(i, queue) 
    threads.append(thread)

if __name__ == "__main__":
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print "all over"

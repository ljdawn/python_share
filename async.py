import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
import functools

def fetch():
    response = yield functools.partial(AsyncHTTPClient().fetch, 'http://jinri.info')
    print response

gen = fetch()
f = gen.next()

def callback(response):
    try:
        gen.send(response)
    except StopIteration:
        pass


f(callback)
print 'here'

tornado.ioloop.IOLoop.instance().start()

from __future__ import absolute_import

import sys
sys.path = ['.'] + sys.path

import tornado.ioloop
import tornado.web

from cult.worker import worker

class MapHandler(tornado.web.RequestHandler):
    def get(self):
        worker.map_and_push()
        self.write('done\n')

class ProcessHandler(tornado.web.RequestHandler):
    def get(self):
        worker.pop_and_process()
        self.write('done\n')

def worker_server():
    application = tornado.web.Application([
        (r"/map", MapHandler),
        (r"/process", ProcessHandler),
    ], **{
        'cookie_secret': 'not-really-secure-will-read-from-env-later'
    })
    application.listen(8888)
    print(' => Listening on 8888')
    tornado.ioloop.IOLoop.instance().start()

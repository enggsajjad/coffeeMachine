import os

import tornado.ioloop
import tornado.web
import atexit

from tornado.options import define, options, parse_command_line


define("port", default=8888, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.write("This is your response")
        self.finish()
    def post(self):
        token = self.get_argument("token", default=None, strip=False)
        if os.path.isfile("/home/pi/CoffeeMachine/UI/userUID.png"):
           self.write("Sorry, someone is already ordering coffee")
        else :
           self.write("Coffee ordered")
           with open("/home/pi/CoffeeMachine/UI/androidOrder.txt", "w+") as f:
              f.write(token)

app = tornado.web.Application([
    (r'/', IndexHandler),
])

def stop_server():
    tornado.ioloop.IOLoop.instance().stop()

def tornadoServer():
    atexit.register(stop_server)
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

tornadoServer()

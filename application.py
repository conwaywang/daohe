# -*- codeing:utf-8 -*-
'''
Created on 2013-9-20

@author: lenovo
'''

import os.path
import tornado.web
import tornado.httpserver

from tornado.options import define, options
from database.dbhelper import dbConnection
from handler.home import MainHandler,RegisterHandler, LoginHandler,\
    LogoutHandler
import settings
from handler.chat import CreateRoomHandler, JoinRoomHandler, LeaveRoomHandler,\
    DissolutionRoomHandler

define('port', default=8888, help='run on the given port', type=int)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                    (r'/register', RegisterHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/create_room", CreateRoomHandler),
                    (r"/join_room", JoinRoomHandler),
                    (r"/leave_room", LeaveRoomHandler),
                    (r"/dissolution_room", DissolutionRoomHandler)
            ]
        
        setting = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=False,
                cookie_secret='11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
                login_url='/login',
                autoescape=None
            )
        settings.mongoDB = dbConnection()
        
        tornado.web.Application.__init__(self, handlers, **setting)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()
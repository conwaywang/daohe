# -*- coding : utf-8 -*-
'''
Created on 2013-9-20

@author: lenovo
'''

import tornado.web
import json
from model.room import Room
from model.user import User
from model.message import Message

class BaseHandler(tornado.web.RequestHandler):
    @property
    def room_dal(self): return Room()
    
    @property
    def user_dal(self): return User()
    
    @property 
    def message_dal(self): return Message()
    
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.user_dal.get_user(int(user_id))
        
    def response(self, state_code, **data):
        result = {"state":state_code}
        if data:
            result = dict(result, **data)
        
        self.write(json.dumps(result))
        
        return
    
        
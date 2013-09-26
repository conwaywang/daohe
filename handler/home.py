# -*- coding : utf-8 -*-
'''
Created on 2013-9-21

@author: lenovo
'''
import json
from base import BaseHandler
from model.user import User
from const_var import ERROR_NAME_FORMAT, ERROR_PASSWORD_FORMAT, ERROR_USER_EXIST,\
    ERROR_ADD_USER, ADD_USER_SUCC, LOGIN_FAILED, LOGIN_SUCC, SUCCESS

class MainHandler(BaseHandler):
    def get(self):
        name = self.get_argument("name")
        
        if name:
            response = {
                    "name": name,
                    "state": 'test'
                }
            self.write(json.dumps(response))
        else:
            self.set_status(404)
            
class RegisterHandler(BaseHandler):
    
    def get(self):
        error_code = 0
        name = self.get_argument("name")
        password = self.get_argument("password")
        if not name or len(name) < 6 :
            error_code = ERROR_NAME_FORMAT
            self.response(error_code)
            return
        if not password or len(password) < 6:
            error_code = ERROR_PASSWORD_FORMAT
            self.response(error_code)
            return
        user = self.user_dal.get({"name":name})
        if user:
            error_code = ERROR_USER_EXIST
            self.response(error_code)
            return
        user = self.user_dal.template()
        user["name"] = name
        user['password'] = password
        user_id = self.user_dal.insert(user)
        if not user_id:
            error_code = ERROR_ADD_USER
            self.response(error_code)
            return
        self.set_secure_cookie("user", str(user_id), expires_days=30)
        self.response(ADD_USER_SUCC)
        
class LoginHandler(BaseHandler):
    
    def get(self):
        name = self.get_argument("name")
        password = self.get_argument("password")
        parameters = {"name": name, "password": password}
        user = self.user_dal.get(parameters)
        if not user:
            self.response(LOGIN_FAILED)
            return
        self.set_secure_cookie("user", str(user["_id"]), expires_days=30)
        #print "get_secure_cookie", self.get_secure_cookie("user")
        self.response(LOGIN_SUCC)
        return
        
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.response(SUCCESS) 
        return       
        

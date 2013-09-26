#-*- coding: utf-8 -*-
'''
Created on 2013-9-26

@author: lenovo
'''
import tornado.web
from handler.base import BaseHandler
from const_var import SUCCESS


##获取离线消息
class GetOffLineMessageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = self.current_user["_id"]
        messages = self.message_dal.get_offline_messages(user_id)
        self.response(SUCCESS, messages)

#发送消息
class SendMsgHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = self.current_user["_id"]
        to_uid = self.get_argument("to_uid")
        
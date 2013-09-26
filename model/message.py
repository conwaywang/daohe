#-*- coding:utf-8 -*-
'''
Created on 2013-9-26

@author: lenovo
'''
import time
from model import Model
from const_var import TABLE_MESSAGE

class Message(Model):
    table = TABLE_MESSAGE
    '''
        {
            uid
            messages:[
                {
                    from_uid,
                    message,
                    time
                }
            ]
        }
    '''
    
    #
    def add_offline_message(self, from_uid, to_uid, message):
        cur_time = time.time()        
        message = {
                   "from_uid": from_uid,
                   "message": message,
                   "time": cur_time
                }
        parameters = {"_id": to_uid}
        update = {
                  "$push":{
                           "messages": message
                        }
                }
        self.find_and_modify(parameters, update)
        
    #
    def get_offline_messages(self, user_id):
        messages = []
        parameters = {"_id": user_id}
        result = self.query(parameters, 0, 1000)   #获取所有离线数据
        if result and len(result):
            messages = [r for r in result]
        return messages
    
    #
    def delete_offline_messages(self, user_id):
        parameters = {"_id": user_id}
        self.remove(parameters)
        
    
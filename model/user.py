#-*- coding: utf-8 -*-
'''
Created on 2013-9-21

@author: lenovo
'''

from model import Model
from const_var import TABLE_USER, MAX_ROOM_NUM_PER_USER, MAX_JOIN_ROOM_NUM

class User(Model):
    table = TABLE_USER
    
    def template(self):
        user = {
            "_id": self.get_id(),
            "name": '',
            "password": '',
            "open": '',
            "photo_url": '',
            "likes": 0,
            "room_list": []
            #black_list
            #black_by_list
            #join_room_list
        }
        return user
    
    def update_user(self, user):
        parameters = {"_id":user["_id"]}
        return self.update(parameters, user)
    
    def get_user(self, user_id):
        parameters = {"_id": int(user_id)}
        return self.get(parameters)
    
    def get_users_count(self):
        parameters = None
        return self.get_count(parameters)
    
    #判断是否有权限创建聊天
    def is_create_room_able(self, user_id):
        parameters = {"_id": user_id}
        result = self.get(parameters)
        if result.has_key('room_list') and len(result['room_list']) >= MAX_ROOM_NUM_PER_USER:
            return False
        return True
    
    #创建room
    def create_room(self, user_id, room_id):
        parameters = {"_id": user_id}
        update = {"$addToSet":{"room_list": room_id}}
        self.update(parameters, update)
        
        
    #拉黑用户
    def set_user_black(self, user_id1, user_id2):
        #step1 user_id2 放入user_id1的black_list
        parameters = {"_id": user_id1}
        update = {"$addToSet":{"black_list": user_id2}}
        self.update(parameters, update)
        #step2 user_id1 放入 user_id2的black_by_list
        parameters = {"_id": user_id2}
        update = {"$addToSet":{"black_by_list": user_id1}}
        self.update(parameters, update)
        
    #判断user_id2是否可以加入user_id1创建的聊天
    def is_room_joinable(self, user_id1, user_id2):
        parameters = {"_id": user_id1, "black_list": user_id2}
        result = self.get(parameters)
        
        if result and len(result):
            return False
        return True
    
    #user加入聊天
    def user_join_room(self, user_id, room_id):
        parameters = {"_id": user_id}
        update = {"$addToSet": {"join_room_list": room_id}}
        self.update(parameters, update)
        
    #判断user是否还能够加入room. res: 1 已经加入  2加入数量超过限制 0-可以加入
    def is_user_can_join_room(self, user_id, room_id):
        parameters = {"_id": user_id}
        fields = {"join_room_list": 1}
        result = self.get(parameters, fields)
        if result and len(result):
            room_list = result["join_room_list"]
            if room_list and len(room_list):
                if room_id in room_list:
                    return 1
                if len(room_list) >= MAX_JOIN_ROOM_NUM:
                    return 2
        return 0    
    
    #guest 离开room
    def leave_room(self, user_id, room_id):
        parameters = {"_id": user_id}
        update = {
                "$pull": {"join_room_list": room_id}
            }
        self.update(parameters, update)
        
    
    

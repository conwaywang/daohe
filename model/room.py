#-*- coding:utf-8 -*-
'''
Created on 2013-9-21

@author: lenovo
'''

import time
from model import Model
from const_var import ROOM_STATE_FREE, ROOM_STATE_CHATTING, TABLE_ROOM, TABLE_USER

class Room(Model):
    table = TABLE_ROOM
    
    #
    def create_room(self, user_id, tags, des):
        cur_time = time.time()
        room = {
            "_id": self.get_id(),
            "des": "",
            "tags": tags,
            "state": ROOM_STATE_FREE,
            "create_time": cur_time,
            "create_user": self.dbref(self.table, user_id)
        }
        return self.insert(room)
        
    #得到room
    def get_room_by_id(self, room_id):
        parameters = {"_id", room_id}
        return self.get(parameters)
            
    #
    def get_rooms_by_tags(self, tags, offset=0, limit=10):
        rooms = []
        parameters = {
                      "tags":{"$all": tags},
                      "state": ROOM_STATE_FREE
                    }
        result = self.query(parameters, offset, limit)
        
        if result and len(result):
            rooms = [r for r in result]
        return rooms
        
    #加入聊天    
    def join_room(self, room_id, guest_id):
        parameters = {"_id", room_id}
        update = {
                  '$set': {'state': ROOM_STATE_CHATTING}, 
                  '$set': {'guest_user': self.dbref(TABLE_USER, guest_id)}
                  }
        self.update(parameters, update)
        
    #判断room 状态是否可以加入
    def is_room_joinable(self, room_id):
        parameters = {"_id", room_id}
        result = self.get(parameters)
        if result and len(result):
            if ROOM_STATE_FREE == result['state']:
                return True
        return False    
    
    #guest离开room
    def leave_room(self, room_id, guest_id):
        parameters = {"_id", room_id}
        update = {
                '$set': {'state': ROOM_STATE_FREE},
                '$unset': {'guest_user': 1}
            }
        self.update(parameters, update);
    
    
#-*- coding: utf-8 -*-
'''
Created on 2013-9-21

@author: lenovo
'''
import tornado.web
from handler.base import BaseHandler

from const_var import ERROR_CR_ID, ERROR_CR_TAGS, ERROR_CR_ROOM_LIMIT, SUCCESS,\
    ERROR_JR_PARAS, ERROR_JR_ROOM_STATE, ERROR_JR_NOT_PERMIT,\
    ERROR_JR_GUEST_ROOM_LIMIT, ERROR_JR_JOIN_ALREADY

#创建聊天
class CreateRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = self.current_user["_id"]
        room_desc = self.get_argument("room_desc")
        room_tags = self.get_argument("room_tags")
        
        if not user_id:
            self.response_state(ERROR_CR_ID)
            return
        if not room_tags:
            self.response_state(ERROR_CR_TAGS)
            return
        
        #step1  judge user has create room
        if not self.user_dal.is_create_room_able(user_id):
            self.response_state(ERROR_CR_ROOM_LIMIT)
            return
        #step2 create room
        tag_list = room_tags.split(";")
        room_id = self.room_dal.create_room(user_id, tag_list, room_desc)
        #step3 update user state
        self.user_dal.create_room(user_id, room_id)
        
        self.response_state(SUCCESS)
        return

#加入聊天
class JoinRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = self.current_user["_id"]
        guest_id = self.get_argument("guest_id")
        room_id = self.get_argument("room_id")
        if not guest_id or not room_id:
            self.response_state(ERROR_JR_PARAS)
            return
        #step1  judge room state 
        if not self.room_dal.is_room_joinable(room_id):
            self.response_state(ERROR_JR_ROOM_STATE)
            return
        #step2 judge black
        if not self.user_dal.is_room_joinable(user_id, guest_id):
            self.response_state(ERROR_JR_NOT_PERMIT)
            return
        #step3 judge guest state
        res = self.user_dal.is_user_can_join_room(guest_id, room_id)
        if 2 == res:
            self.response_state(ERROR_JR_GUEST_ROOM_LIMIT)
            return
        if 1 == res:
            self.response_state(ERROR_JR_JOIN_ALREADY)
            return
        
        self.room_dal.join_room(room_id, guest_id)

#guest离开聊天
class LeaveRoomHandler(BaseHandler):
    def get(self):
        room_id = self.get_argument("room_id")
        guest_id = self.current_user["_id"]
        
        # 解除room的限定
        self.room_dal.leave_room(room_id, guest_id)
        # 
        self.user_dal.leave_room(guest_id, room_id)

#创立者离开
class DissolutionRoomHandler(BaseHandler):
    def get(self):
        pass


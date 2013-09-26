# -*- coding : utf-8 -*-
'''
Created on 2013-9-24

@author: lenovo
'''
import json
import tornado.web
from base import BaseHandler
from model.room import Room
from const_var import ERROR_SR_KEY

#
class SearchHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        offset = int(self.get_argument("offset"))
        limit = int(self.get_argument("size"))
        search_key = self.get_argument("key").strip()
        divider = ";;"  #
        
        if not search_key:
            self.response(ERROR_SR_KEY)
            return
        tag_list = search_key.split(divider)
        rooms = self.room_dal.get_rooms_by_tags(tag_list, offset, limit)
        self.write(json.dumps(rooms))
        
    
        
        
        
    
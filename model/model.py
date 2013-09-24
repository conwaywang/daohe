# -*- coding : utf-8 -*-
'''
Created on 2013-9-20

@author: lenovo
'''

from database.dbhelper import Database

from bson.dbref import DBRef
from bson.timestamp import Timestamp
import datetime

class Model(object):
    table = None
    
    @property
    def db(self): return Database()
    
    def dbref(self, table, object_id):
        return DBRef(table, object_id)
    
    @property
    def timestamp(self):
        return Timestamp(datetime.datetime.now(), 0)
    
    def insert(self, documents):
        return self.db.insert(self.table, documents)
    
    def get(self, parameters, fields=None):
        return self.db.find_one(self.table, parameters, fields)
    
    def get_id(self):
        return self.db.get_id(self.table)
    
    def query(self, parameters, offset=0, limit=10, fields=None):
        result = []
        cursor = self.db.query(self.table, parameters, offset, limit, fields)
        if cursor and cursor.count():
            result = [item for item in cursor]
        return result
    
    def get_count(self, parameters):
        return self.db.get_count(self.table, parameters);
    
    def remove(self, parameters):
        return self.db.remove(self.table, parameters)

    def update(self, parameters, update):
        return self.db.update(self.table, parameters, update)
    
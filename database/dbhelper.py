# -*- coding: utf-8 -*-
'''
Created on 2013-9-20

@author: lenovo
'''

import pymongo
import settings
from pymongo.son_manipulator import AutoReference, NamespaceInjector

def dbConnection():
    host = settings.MONGODB_SETTINGS['host']
    port = settings.MONGODB_SETTINGS['port']
    max_pool = settings.MONGODB_SETTINGS['max_pool']
    connection = pymongo.Connection(host, port, max_pool)
    db = connection["chat"]
    db.add_son_manipulator(AutoReference(db))
    return db


class Database(object):
    def __init__(self):
        self.db = settings.mongoDB
        
    def insert(self, table, documents):
        return self.db[table].insert(documents)
    
    def query(self, table, parameters, offset, limit, fields=None):
        cursor = self.db[table].find(parameters, fields)\
            .skip(offset).limit(limit)
        #cursor.sort(sort, pymongo.DESCENDING)
        return cursor
    
    def get_count(self, table, parameters):
        return self.db[table].find(parameters).count()
    
    def get_id(self, table):
        value = self.db["ids"].find_and_modify({"name":table}, {'$inc': {"value":1}}, new=True, upsert=True)
        return value['value']
        
        
    def find_one(self, table, parameters, fields=None):
        return self.db[table].find_one(parameters, fields)
    
    def update(self, table, parameters, update, safe=True):
        return self.db[table].update(parameters, update, safe)
    
    def dereference(self, dbref):
        return self.db.dereference(dbref)
    
    def remove(self, table, parameters):
        self.db[table].remove(parameters)
    
    

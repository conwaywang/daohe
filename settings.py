# -*- coding: utf-8 -*-
'''
Created on 2013-9-20

@author: lenovo
'''
import os.path

# mongo db
MONGODB_SETTINGS = {
    'host': '127.0.0.1',
    'port': 27017,
    'max_pool': 300
}

# pagination
MINI_PAGE_SIZE = 20
MAX_PAGE_SIZE = 5 * MINI_PAGE_SIZE


mongoDB = None
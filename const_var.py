#-*- coding:utf-8 -*-
'''
Created on 2013-9-21

@author: lenovo
'''
#table
TABLE_USER = 'user'
TABLE_ROOM = 'room'

#room max num
MAX_ROOM_NUM_PER_USER = 1
#能加入的最大room数
MAX_JOIN_ROOM_NUM = 1




#room 状态
ROOM_STATE_FREE = 0 #空闲
ROOM_STATE_UNAVLIABLE = -1 #废弃
ROOM_STATE_CHATTING = 1 #正在聊天

#web request success
SUCCESS = 0

#register error code
ADD_USER_SUCC = 0
ERROR_NAME_FORMAT = 101
ERROR_PASSWORD_FORMAT = 102
ERROR_USER_EXIST = 103
ERROR_ADD_USER = 104

#login error code
LOGIN_SUCC = 0
LOGIN_FAILED = 201

#create room
ERROR_CR_ID = 301
ERROR_CR_TAGS = 302
ERROR_CR_ROOM_LIMIT = 303

#join room
ERROR_JR_PARAS = 401
ERROR_JR_ROOM_STATE = 402
ERROR_JR_NOT_PERMIT = 403
ERROR_JR_GUEST_ROOM_LIMIT = 404   #用户能加入的room限制
ERROR_JR_JOIN_ALREADY = 405 #已经加入

#search room
ERROR_SR_KEY = 501

#dissolution room
ERROR_DR_ROOM_ID = 601

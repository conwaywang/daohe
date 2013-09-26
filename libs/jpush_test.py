#-*- coding: utf8 -*-
'''
Created on 2013-9-26

@author: lenovo
'''
import jpush

SENDNO = 111
DES="description"
TITLE="Python API"
CONTENT="Testing Python API"

jp = jpush.JpushClient('username', 'password', 'url')
jp.send_notification_with_tag('tags', 'appkeys', SENDNO, DES, TITLE, CONTENT, 'android')
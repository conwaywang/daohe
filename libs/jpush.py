#-*- coding: utf8 -*-

# A lightweight wrapper for remote Jpush API
# Details refer to http://docs.jpush.cn/pages/viewpage.action?pageId=557084

import hashlib
import urllib
import urllib2
import json
import tornado.httpclient


class JpushClient:
    def __init__(self, username, password, callback_url=""):
        self.username = username
        self.password = password
        self.callback_url = callback_url
        #self.url = "http://api.jpush.cn:8800/sendmsg/sendmsg"
        self.url = "http://api.jpush.cn:8800/sendmsg/v2/sendmsg"

    def build_params(self, kargs):
        params = {}
        params["username"] = self.username
        params["callback_url"] = self.callback_url
        params["sendno"] = kargs["sendno"]
        params["appkeys"] = kargs["appkeys"]
        params["receiver_type"] = kargs["receiver_type"]
        params["receiver_value"] = kargs["receiver_value"]
        params["verification_code"] = kargs["verification_code"]
        params["msg_type"] = kargs["msg_type"]
        params["msg_content"] = json.dumps(kargs["msg_content"])
        params["send_description"] = kargs["senddes"]
        params["platform"] = kargs["device"]
        return params


    def build_content(self, title, content, type):
        if type == 1:   # notification
            return {"n_title": title, "n_content": content}
        else:           # custom message
            return {"title": title, "message": content}


    def generate_verification_code(self, sendno, receiver_type, receiver_value):
        m = hashlib.md5()
        m2 = hashlib.md5()
        m.update(self.password)
        input = "%s%d%d%s%s" % (self.username, sendno, receiver_type, receiver_value, m.hexdigest().upper())
        m2.update(input)
        return m2.hexdigest().upper()


    def send_notification_with_imei(self, imei, appkeys, sendno, 
                                    senddes, msgtitle, 
                                    msg_content, device):
        '''Send notification with imei id'''
        receiver_type = 1
        msg_type = 1
        msg_content = self.build_content(msgtitle, msg_content, msg_type)
        receiver_value = imei
        verification_code = self.generate_verification_code(sendno, receiver_type, receiver_value)
        params = self.build_params(locals())
        self.send_msg(params)


    def send_custom_msg_with_imei(self, imei, appkeys, sendno, 
                                    senddes, msgtitle, 
                                    msg_content, device):
        '''Send custom message with imei id'''
        receiver_type = 1
        msg_type = 2
        msg_content = self.build_content(msgtitle, msg_content, msg_type)
        receiver_value = imei
        verification_code = self.generate_verification_code(sendno, receiver_type, receiver_value)
        params = self.build_params(locals())
        self.send_msg(params)


    def send_notification_with_tag(self, tag, appkeys, sendno, 
                                    senddes, msgtitle, 
                                    msg_content, device):
        '''Send notification with tag'''
        receiver_type = 2
        msg_type = 1
        msg_content = self.build_content(msgtitle, msg_content, msg_type)
        receiver_value = tag
        verification_code = self.generate_verification_code(sendno, receiver_type, receiver_value)
        params = self.build_params(locals())
        self.send_msg(params)


    def send_custom_msg_with_tag(self, tag, appkeys, sendno, 
                                    senddes, msgtitle, 
                                    msg_content, device):
        '''Send custom message with tag'''
        receiver_type = 2
        msg_type = 2
        msg_content = self.build_content(msgtitle, msg_content, msg_type)
        receiver_value = tag
        verification_code = self.generate_verification_code(sendno, receiver_type, receiver_value)
        params = self.build_params(locals())
        self.send_msg(params)


    def send_notification_with_alias(self, alias, appkeys, sendno, 
                                    senddes, msgtitle, 
                                    msg_content, device):
        '''Send notification with alias'''
        receiver_type = 3
        msg_type = 1
        msg_content = self.build_content(msgtitle, msg_content, msg_type)
        receiver_value = alias
        verification_code = self.generate_verification_code(sendno, receiver_type, receiver_value)
        params = self.build_params(locals())
        self.send_msg(params)


    def send_custom_msg_with_alias(self, alias, appkeys, sendno, 
                                    senddes, msgtitle, 
                                    msg_content, device):
        '''Send custom message with alias'''
        receiver_type = 3
        msg_type = 2
        msg_content = self.build_content(msgtitle, msg_content, msg_type)
        receiver_value = alias
        verification_code = self.generate_verification_code(sendno, receiver_type, receiver_value)
        params = self.build_params(locals())
        self.send_msg(params)


    def send_notification_with_appkey(self, appkeys, sendno, 
                                    senddes, msgtitle, 
                                    msg_content, device):
        '''Send notification with appkey'''
        receiver_type = 4
        msg_type = 1
        msg_content = self.build_content(msgtitle, msg_content, msg_type)
        receiver_value = ""
        verification_code = self.generate_verification_code(sendno, receiver_type, receiver_value)
        params = self.build_params(locals())
        self.send_msg(params)


    def send_custom_msg_with_appkey(self, appkeys, sendno, 
                                    senddes, msgtitle, 
                                    msg_content, device):
        '''Send custom message with appkey'''
        receiver_type = 4
        msg_type = 2
        msg_content = self.build_content(msgtitle, msg_content, msg_type)
        receiver_value = ""
        verification_code = self.generate_verification_code(sendno, receiver_type, receiver_value)
        params = self.build_params(locals())
        self.send_msg(params)


    def send_msg(self, params):
        '''Push API for all kinds of message and notification, dict params restore all parameters'''
        try:
            f = urllib2.urlopen(
                    data = urllib.urlencode(params),
                    url = self.url
                )
        except:
            print "网络无法访问"
        else:
            result = json.loads(f.read())
            if result.get("errcode") == 0:
                print u"发送成功, sendNo=%s" % result.get("sendno")
            else:
                print u"发送失败，错误代码=%s, 错误消息=%s" % (result.get("errcode"), result.get("errmsg"))
        finally:
            f.close()
            
    
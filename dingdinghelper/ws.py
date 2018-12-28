#!/usr/bin/env python3
#coding=utf-8
# => Author: Abby Cin
# => Mail: abbytsing@gmail.com
# => Created Time: Sat 31 Mar 2018 12:45:38 PM CST

import json
import time
import math
import random
import requests
import sys

from websocket import create_connection

class Message():
    def __init__(self, phone, password):
        self.phone = "+86-" + str(phone)
        self.passwd = password
        self.token = None
        self.app_key = "85A09F60A599F5E1867EAB915A8BB07F"
        self.device_id = "05b6bbf32bb34d0eb6a5435d28452b79"
        self.reg = {
            "lwp":"/reg","headers": { 
                "cache-header": "token app-key did ua vhost wv",
                "vhost":"WK",
                "ua":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OS(windows/6.1) Browser(chrome/65.0.3325.181) DingWeb/3.6.3 LANG/zh_CN",
                "app-key": self.app_key,
                "wv":"im:3,au:3,sy:4",
                "did": self.device_id,
                "mid":"f61f0002 0"
            },
            "body":None
        }
        self.keep_alive = {
            "lwp":"/!",
            "headers": { 
                "mid":"fb420007 0"
            },
            "body": None
        }
        self.check_license = {
            "lwp":"/r/Adaptor/LoginI/checkLicense",
            "headers": {
                "mid":"9113001a 0"
            },
            "body": [self.phone, 0]
        }
        self.login = {
            "lwp":"/r/Adaptor/LoginI/login",
            "headers": {
                "mid":"639c001b 0"
            },
            "body": [
                {
                    "title":"Windows 7 Web",
                    "model":"Windows 7",
                    "token":""
                },
                self.phone,
                self.passwd,
                self.app_key,
                None
            ]
        }
        self.sms_code =  {
            "lwp":"/r/Adaptor/LoginI/sendSmsCode",
            "headers": {
                "mid":"1a0d001c 0"
            },
            "body": [self.phone]
        }
        self.token_login = {
            "lwp":"/r/Adaptor/LoginI/tokenLogin",
            "headers": { "mid":"a62a0020 0" },
            "body":[
                {
                    "title":"Windows 7 Web",
                    "model":"Windows 7",
                    "token":""
                },
                self.phone,
                "5769", # sms code
                self.app_key,
                "0", 
                None
            ]
        }
        self.subsribe = {
            "lwp":"/subscribe",
            "headers": {
                "token":"access token of login response",
                "sync":"0,0;0;0;",
                "set-ver":"0",
                "mid":"b91b000d 0"
            }
        }
        self.switch_status = {"lwp":"/r/Sync/getSwitchStatus","headers":{"mid":"0b75000e 0"},"body":[]}
        self.confirm_info = {"lwp":"/r/Adaptor/IDLDing/getConfirmStatusInfo","headers":{"mid":"98d9000f 0"},"body":[]}
        self.accept_license = {"lwp":"/r/Adaptor/LoginI/acceptLicense","headers":{"mid":"caae001f 0"},"body":[self.phone,0]}
        self.create_session = {
            "lwp":"/r/Adaptor/LoginI/createTempSessionInfo",
            "headers": {
                "mid":"f6970023 0"
            },
            "body":[]
        }

    def get_did(self):
        return self.device_id

    def get_mid(self):
        curr = int(time.time())
        return hex(curr)[2:] + " 0"

    def get_random(self):
        return str(math.ceil(time.time() * 1e3)) + str(math.ceil(random.random() * 1e3))

    def get_token(self):
        """return a fixed token at present"""
        if self.token == None:
            self.token = "C1522630905670449661624441522635142573234"
            #self.token = "C{start}05444427{end}".format(start = self.get_random(), end = self.get_random())
        return self.token

    def get_reg_msg(self):
        reg = self.reg
        reg["mid"] = self.get_mid()
        return reg

    def get_keepalive_msg(self):
        res = self.keep_alive
        res["mid"] = self.get_mid()
        return res

    def get_check_license_msg(self):
        res = self.check_license
        res["mid"] = self.get_mid()
        return res

    def get_login_msg(self):
        res = self.login
        res["headers"]["mid"] = self.get_mid()
        res["body"][0]["token"] = self.get_token()
        return res

    def get_sms_code_msg(self):
        res = self.sms_code
        res["headers"]["mid"] = self.get_mid()
        return res

    def get_token_login_msg(self):
        res = self.token_login
        res["headers"]["mid"] = self.get_mid()
        code = input("enter sms code: ")
        res["body"][2] = code
        res["body"][0]["token"] = self.get_token()
        return res

    def get_subscribe_msg(self, access_token):
        res = self.subsribe
        res["headers"]["token"] = access_token
        res["headers"]["mid"] = self.get_mid()
        return res

    def get_switch_status_msg(self):
        res = self.switch_status
        res["headers"]["mid"] = self.get_mid()
        return res

    def get_confirm_msg(self):
        res = self.confirm_info
        res["headers"]["mid"] = self.get_mid()

    def get_create_session_msg(self):
        res = self.create_session
        res["headers"]["mid"] = self.get_mid()
        return res

    def get_accept_license_msg(self):
        res = self.accept_license
        res["headers"]["mid"] = self.get_mid()
        return res        

def get_cookie(phone, password):
    host_list = ["wss://webalfa-cm3.dingtalk.com", "wss://webalfa-cm10.dingtalk.com", "wss://webalfa.dingtalk.com"]
    ws = None
    for host in host_list:
        ws = create_connection(host)
        if ws.connected:
            break
    
    if ws == None or ws.connected == False:
        print("can't connect to these hosts: {h}".format(h = host_list))
        sys.exit(1)
    
    msg = Message(phone, password)

    ws.send(json.dumps(msg.get_reg_msg()))
    ws.recv()

    ws.send(json.dumps(msg.get_check_license_msg()))
    ws.recv()

    ws.send(json.dumps(msg.get_login_msg()))
    res = json.loads(ws.recv())
        
    while res["code"] == 400:
        print(res["body"]["reason"])
        ws.send(json.dumps(msg.get_sms_code_msg()))
        ws.recv()
        ws.send(json.dumps(msg.get_token_login_msg()))
        res = json.loads(ws.recv())

    token = res["body"]["accessToken"]

    ws.send(json.dumps(msg.get_subscribe_msg(access_token = token)))
    ws.recv()

    ws.send(json.dumps(msg.get_switch_status_msg()))
    ws.recv()

    ws.send(json.dumps(msg.get_confirm_msg()))
    ws.recv()
    ws.recv() # why response twice ??

    ws.send(json.dumps(msg.get_create_session_msg()))
    res = json.loads(ws.recv())
    if res["code"] == 400:
        print(res["body"]["reason"])
    
    sid = res["headers"]["sid"]

    # create tmp session
    header = {
        "Host": "login.dingtalk.com",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 OS(windows/6.1) Browser(chrome/65.0.3325.181) DingWeb/3.6.3 LANG/zh_CN",
        "Accept": "*/*",
        "Referer": "https://im.dingtalk.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "deciveid={did}; deviceid_exist=true; dd_sid={session_id}".format(did = msg.device_id, session_id = sid)
    }

    tmp = str(math.ceil(time.time() * 1e3))
    payload = {
        "callback": "jQuery19104339311785622433_{t}".format(t = tmp),
        "sessionId": res["body"],
        "_": "{t}".format(t = tmp)
    }
    resp = requests.get("https://login.dingtalk.com/login/createSessionInfoByTemp.jsonp", params=payload, headers = header)
    dt_s = resp.headers.get("Set-Cookie").split(';')[0]

    # build cookie
    cookie_factory = "deviceid={did}; deviceid_exist=true; up_ab=y; preview_ab=y; dd_sid={session_id}; {dts}"
    cookie = cookie_factory.format(did = msg.device_id, session_id = sid, dts = dt_s)
    return cookie

def renew_cookie(cookie_filepath, ding_username, ding_password):
    cookie = get_cookie(ding_username, ding_password)
    expiration_time = math.ceil(time.time())
    try:
        fd = open(cookie_filepath, 'w')
        data = {"expiration": expiration_time, "cookie": cookie}
        fd.write(json.dumps(data))
        fd.close()
    except Exception as e:
        print("Error: {err}".format(err = e.args))
        sys.exit(1)
    return cookie

def generate_cookie(cookie_filepath, phone, password):
    week_sec = 60 * 60 * 24 * 6
    tmp = None
    try:
        with open(cookie_filepath, 'r') as fd:
            tmp = fd.read()
            fd.close()
    except Exception:
        return renew_cookie(cookie_filepath, phone, password)

    data = json.loads(tmp)
    cookie = data["cookie"]
    # check if cookie valid
    now = math.ceil(time.time())
    old = int(data["expiration"])
    if now - old > week_sec:
        cookie = renew_cookie(cookie_filepath, phone, password)
    return cookie

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("%s phone password" %(sys.argv[0]))
        sys.exit(1)

    print(get_cookie(sys.argv[1], sys.argv[2]))
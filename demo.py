'''
@File: dirty_demo.py
@Description: Demo
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2020-02-11 15:33:59
'''

import requests
import json
from dingdinghelper import DingDingHelper

if __name__ == "__main__":
  ding = DingDingHelper()
  ding.corpid = 'ding428c9b6bb8962a4d35c2f4657eb6378f'
  ding.corpsecret = 'L8v6TYuSnjq8VsErPiCoJdWU19T5Embn1P8KW7IyO3_FkJw_ZLPqdKt6blQwwd34'
  ding.msgurl = "https://oapi.dingtalk.com/robot/send?access_token=e02a2c7de529ca83ba5d4e6f6c37b31f53152b3dc54d30653ed2235723027651",
  # ding.send_msg('DingDingHelper Test')
  r = requests.get("http://139.196.104.13:9181/api/_/dingding/getCookie")
  if r.status_code != 200:
    exit(1)
  r_data = json.loads(r.content)
  ding.cookie = r_data["data"].rstrip()
  print(ding.cookie)
  ding.upload_file("D:/SocketTest3.zip", 483476421, '/topjs/topjs3/windows/')
  # ding.renew_cookie()
  # print(ding.cookie)
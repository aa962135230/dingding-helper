'''
@File: demo.py
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2018-12-28 02:17:37
'''

from dingdinghelper import DingDingHelper

if __name__ == "__main__":
  ding = DingDingHelper()
  ding.username = '13712345678'
  ding.password = 'xxx'
  ding.corpid = 'xxx'
  ding.corpsecret = 'xxx'
  ding.msgurl = 'https://oapi.dingtalk.com/robot/send?access_token=xxx'
  # ding.send_msg('DingDingHelper Test')
  # ding.upload_file("E:/xxx.zip", 483476421, '/topjs/topjs3/windows/')
  ding.renew_cookie()
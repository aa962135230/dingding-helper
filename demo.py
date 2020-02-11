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
  ding.corpid = 'ding428c9b6bb8962a4d35c2f4657eb6378f'
  ding.corpsecret = 'L8v6TYuSnjq8VsErPiCoJdWU19T5Embn1P8KW7IyO3_FkJw_ZLPqdKt6blQwwd34'
  ding.msgurl = 'https://oapi.dingtalk.com/robot/send?access_token=e02a2c7de529ca83ba5d4e6f6c37b31f53152b3dc54d30653ed2235723027651'
  # ding.send_msg('DingDingHelper Test')
  # ding.upload_file("E:/xxx.zip", 483476421, '/topjs/topjs3/windows/')
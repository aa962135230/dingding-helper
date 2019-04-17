'''
@File: demo.py
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2018-12-28 02:17:37
'''

import json, os
from dingdinghelper import DingDingHelper

if __name__ == "__main__":
  if not os.path.exists('dingding.cfg'):
    print('Error: dingding.cfg not found.')
  with open('dingding.cfg', 'r') as f:
    cfg = json.load(f)
  ding = DingDingHelper(cfg)
  # ding.send_msg("这是一条测试消息")
  ding.upload_file("C:/Users/Administrator/Desktop/test.zip")
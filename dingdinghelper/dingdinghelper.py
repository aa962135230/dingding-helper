'''
@File: dingdinghelper.py
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2018-12-27 17:30:23
'''

import os, json
from urllib import request

class DingDingHelper:
  """钉钉助手
  """

  def __init__(self, cfg):
    self._cfg = cfg

  def send_msg(self, msg):
    textmod = {
        "msgtype": "text",
        "text": { "content": msg },
        "at": { "isAtAll": False }
    }
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    req = request.Request(url=self._cfg['msg_url'], data=textmod, headers={
        "Content-Type": "application/json", "charset": "utf-8"
    })
    res = request.urlopen(req)
    res = res.read()
    if not (json.loads(res).get('errmsg') == 'ok'):
        self.send_msg(msg)

if __name__ == "__main__":
  if not os.path.exists('dingding.cfg'):
    print('Error: dingding.cfg not found.')
  with open('dingding.cfg', 'r') as f:
    cfg = json.load(f)
  ding = DingDingHelper(cfg)
  ding.send_msg("这是一条测试消息")
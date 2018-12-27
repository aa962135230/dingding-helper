'''
@File: dingdinghelper.py
@Author: leon.li(l2m2lq@gmail.com)
@Date: 2018-12-27 17:30:23
'''

import os, json
from urllib import request, parse

class DingDingHelper:
  """钉钉助手
  """

  def __init__(self, cfg):
    self._cfg = cfg

  def get_access_token(self):
    self._access_token = ""
    params = parse.urlencode({'corpid': self._cfg['corpid'], 'corpsecret': self._cfg['corpsecret']})
    url = 'https://oapi.dingtalk.com/gettoken?%s' % params
    with request.urlopen(url) as f:
      res = json.loads(f.read().decode('utf-8'))
      if res.get("errmsg") == "ok":
        self._access_token = res.get("access_token")
    return self._access_token

  def send_msg(self, msg):
    data = {
      "msgtype": "text",
      "text": { "content": msg },
      "at": { "isAtAll": False }
    }
    data = json.dumps(data).encode(encoding='utf-8')
    req = request.Request(url=self._cfg['msg_url'], data=data, headers={
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
  # ding.send_msg("这是一条测试消息")
  print(ding.get_access_token())
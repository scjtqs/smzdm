#coding:utf-8
import urllib
import http.cookiejar
import json
from secret import IS_USE_QQ_PUSH
from secret import PUSH_QQ
from secret import PUSH_GROUP
from secret import PUSH_TOKEN
class MsgList:
    msg_list= []

class Qqpush:
    pushurl='https://wx.scjtqs.com/qq/push/pushMsg'
    def notify_qq(self,msg):
        MsgList.msg_list.append(msg)
        self.push(msg)
        self.clear_list()

    def push(self,data):
        if IS_USE_QQ_PUSH!=True:
            return False
        jsonret=''
        if data in MsgList.msg_list:
            return
        if PUSH_QQ>0:
            post = {}
            post['qq'] = PUSH_QQ
            post['content'] = [{"msgtype": "text", "text": data}]
            jsonret=self.post(post)
            print(jsonret)
        if PUSH_GROUP>0:
            post = {}
            post['group'] = PUSH_GROUP
            post['content'] = [{"msgtype": "text", "text": data}]
            jsonret = self.post(post)
            print(jsonret)
        return jsonret

    def post(self,postdata):
        url = self.pushurl+"?token="+PUSH_TOKEN
        postdata=bytes(json.dumps(postdata),'utf8')
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0",
            'Content-Type': 'application/json',
        }
        req = urllib.request.Request(url=url, data=postdata, headers=header)
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        r = opener.open(req)
        response = r.read().decode('utf-8')
        jsonret=json.loads(response)
        return jsonret

    def clear_list(self):
        if len(MsgList.msg_list) > 1000:
            msg_list = MsgList.msg_list[500:]

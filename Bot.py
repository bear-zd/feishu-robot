#!/usr/bin/env python
# --coding:utf-8--

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
import json
from urllib import request, parse

from utils import get_tenant_access_token, isreciept
from Function import *
from Private import APP_VERIFICATION_TOKEN


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 解析请求 body
        req_body = self.rfile.read(int(self.headers['content-length']))
        obj = json.loads(req_body.decode("utf-8"))
        print(req_body)

        # 校验 verification token 是否匹配，token 不匹配说明该回调并非来自开发平台
        token = obj.get("token", "")
        if token != APP_VERIFICATION_TOKEN:
            print("verification token not match, token =", token)
            self.response("")
            return

        # 根据 type 处理不同类型事件
        type = obj.get("type", "")
        if "url_verification" == type:  # 验证请求 URL 是否有效
            self.handle_request_url_verify(obj)
        elif "event_callback" == type:  # 事件回调
            # 获取事件内容和类型，并进行相应处理，此处只关注给机器人推送的消息事件
            event = obj.get("event")
            if event.get("type", "") == "message":
                self.handle_message(event)
                return
        return

    def handle_request_url_verify(self, post_obj):
        # 原样返回 challenge 字段内容
        challenge = post_obj.get("challenge", "")
        rsp = {'challenge': challenge}
        self.response(json.dumps(rsp))
        return

    def handle_message(self, event):
        # 此处只处理 text 类型消息，其他类型消息忽略
        msg_type = event.get("msg_type", "")
        if msg_type == "text":
            # 调用发消息 API 之前，先要获取 API 调用凭证：tenant_access_token
            access_token = get_tenant_access_token()
            if access_token == "":
                self.response("")
                return

            # 机器人回复收到的消息
            if event.get('chat_type') == 'group' and event.get('is_mention') == True:
                open_id = event.get("open_chat_id")
                open_id = {"open_chat_id": open_id}
            else:
                open_id = event.get("open_id")
                open_id = {"open_id": open_id}
            self.msg_compoment(access_token, open_id, event.get("text"))
            self.response("")
            return
        elif msg_type == "image":
            img_key = event.get("image_key")
            reciept = isreciept(f'https://open.feishu.cn/open-apis/image/v4/get?image_key={img_key}')
            if reciept.get('isreciept', False) == True:
                access_token = get_tenant_access_token()
                open_id = event.get("open_id")
                open_id = {"open_id": open_id}
                self.msg_compoment(access_token, open_id, f"发票识别成功，发票号为:{reciept.get('InvoiceCodeConfirm')}")
                self.response("")
                return
            else:
                access_token = get_tenant_access_token()
                open_id = event.get("open_id")
                open_id = {"open_id": open_id}
                self.msg_compoment(access_token, open_id, "目前暂不支持其他图片功能")
                self.response("")
                return



    def response(self, body):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(body.encode())

    def send_message(self, token, open_id, text):
        url = "https://open.feishu.cn/open-apis/message/v4/send/"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }
        req_body = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        req_body = dict(req_body, **open_id)  # 根据open_id判断返回域

        data = bytes(json.dumps(req_body), encoding='utf8')
        req = request.Request(url=url, data=data, headers=headers, method='POST')
        try:
            response = request.urlopen(req)
        except Exception as e:
            print(e.read().decode())
            return

        rsp_body = response.read().decode('utf-8')
        rsp_dict = json.loads(rsp_body)
        code = rsp_dict.get("code", -1)
        if code != 0:
            print("send message error, code = ", code, ", msg =", rsp_dict.get("msg", ""))

    def send_card(self, token, open_id, card):  # 发送卡片
        url = "https://open.feishu.cn/open-apis/message/v4/send/"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + token
        }  # 固定头
        req_body = {
            "msg_type": "interactive",
            "card": card
        }  # 请求体
        req_body = dict(req_body, **open_id)  # 根据open_id判断返回域

        data = bytes(json.dumps(req_body), encoding='utf8')
        req = request.Request(url=url, data=data, headers=headers, method='POST')
        try:
            response = request.urlopen(req)
        except Exception as e:
            print(e.read().decode())
            return

        rsp_body = response.read().decode('utf-8')
        rsp_dict = json.loads(rsp_body)
        code = rsp_dict.get("code", -1)
        if code != 0:
            print("send message error, code = ", code, ", msg =", rsp_dict.get("msg", ""))

    def msg_compoment(self, token, open_id, text):
        if '骚话' in text:
            self.send_message(token, open_id, GetHitokoto())
        elif "wifi" in text:
            self.send_message(token, open_id, GetWIFIPassword())
        elif "github周报" in text:
            GWC = GWCreeper()
            print(GWC)
            for i in GWC:
                self.send_card(token, open_id, i)
        else :
            self.send_message(token, open_id, text)


def run():
    port = 5000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("start.....")
    httpd.serve_forever()


if __name__ == '__main__':
    run()

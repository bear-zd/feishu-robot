import requests
import json
from urllib import request, parse
import base64
import requests
from Private import APP_ID, APP_SECRET


def Img2Binary(url):
    return request.urlopen(url).read()


def get_tenant_access_token():  # 获取token

    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {
        "Content-Type": "application/json"
    }
    req_body = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }

    data = bytes(json.dumps(req_body), encoding='utf8')
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    try:
        response = request.urlopen(req)
    except Exception as e:
        print(e.read().decode())
        return ""

    rsp_body = response.read().decode('utf-8')
    rsp_dict = json.loads(rsp_body)
    code = rsp_dict.get("code", -1)
    if code != 0:
        print("get tenant_access_token error, code =", code)
        return ""
    return rsp_dict.get("tenant_access_token", "")


def ImgUpload(Imgurl):
    url = 'https://open.feishu.cn/open-apis/image/v4/put/'
    token = get_tenant_access_token()
    Imgcontent = Img2Binary(Imgurl)
    headers = {"Authorization": "Bearer " + token}
    files = {"image": Imgcontent}
    data = {"image_type": "message"}
    req = requests.post(url=url, data=data, headers=headers, files=files)
    return req.json()['data']['image_key']

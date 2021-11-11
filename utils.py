import requests
import json
from urllib import request, parse
import base64
import requests
from Private import APP_ID, APP_SECRET, GetAccess


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


def isreciept(ImgUrl):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice"
    # 二进制方式打开图片文件
    if "http" in ImgUrl:
        token = get_tenant_access_token()
        headers = {"Authorization": "Bearer " + token}
        req = request.Request(url=ImgUrl, headers=headers, method='GET')
        img = base64.b64encode(request.urlopen(req).read())

    else :
        img = base64.b64encode(open(ImgUrl, 'rb').read())

    params = {"image": img}
    access_token = GetAccess()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    result = requests.post(request_url, data=params, headers=headers).json()
    if result.get('error_code') != None:
        return {'isreciept':False, 'InvoiceCodeConfirm':None}
    else:
        return {'isreciept':True, 'InvoiceCodeConfirm':result['words_result'].get('InvoiceCodeConfirm','未识别成功')}

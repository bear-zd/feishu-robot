import requests
headers = {'user-agent': 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'} 

def Img2Binary(url):
    r = requests.get(url, headers)
    return r.content

import random
from bs4 import BeautifulSoup
import time
import requests
import json
import urllib.request
import ssl
from CardTemplate import *
from utils import *
from Private import WIFIPW, GithubWeekly


def GetHitokoto():
    # 详细的开发文档： https://developer.hitokoto.cn/sentence/#%E8%AF%B7%E6%B1%82%E5%9C%B0%E5%9D%80
    ssl._create_default_https_context = ssl._create_unverified_context
    type = random.choice(['a', 'c', 'h'])
    keys = {'c': type}
    url = 'https://v1.hitokoto.cn/'
    r = requests.get(url, keys)
    return r.json()['hitokoto']


def GetWIFIPassword():
    return WIFIPW


def GWCreeper():
    # Github 周刊爬虫
    headers = {'user-agent':
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}
    result = []
    year = int(time.strftime("%Y")) % 100
    week = int(time.strftime("%W")) - 1
    if week == 1:
        week = 53
    content = requests.get(f'{GithubWeekly}{year}{week}', headers=headers)
    if content.status_code == 200:
        content = BeautifulSoup(content.text, 'html.parser').findAll(name="div", attrs={'class': 'repo-card'})
        for i in content:
            infor = i.findAll('a')
            head = infor[0].text
            author = infor[1].text.split('@')[1]
            avatarurl = r'https://avatars.githubusercontent.com/' + author + '?size=64'
            imgKey = ImgUpload(avatarurl)
            url = i.a['href']
            description = i.p.text
            lanstar = i.findAll('span',
                                {'class': 'MuiTypography-root MuiTypography-caption MuiTypography-colorTextSecondary'})
            if len(lanstar) == 1:
                star = lanstar[0].text
                language = ''
            else:
                language, star = lanstar[0].text, lanstar[1].text
            result.append(
                ConWithPic(content=f'**{head}**\n{description}\n{url}\n语言：{language}    star：{star}'.replace('\xa0', '')
                           , img_content=f'{head}', img_key=imgKey)
            )
        return result
    else:
        print("现在无法访问或是机器人出现问题，请联系")


def ReceiptUpload():
    pass

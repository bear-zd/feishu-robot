def ConWithPic(content, img_key="img_e344c476-1e58-4492-b40d-7dcffe9d6dfg", img_content='图片'):
    return {"config": {"wide_screen_mode": True},
            "elements": [{"tag": "div", "text": {"tag": "lark_md",
                                                 "content": content},
                          "extra": {"tag": "img", "img_key": img_key,
                                    "alt": {"tag": "plain_text", "content": img_content}}}]}

''' 飞书消息卡片的按钮功能暂且未完善，所以暂且不通过Button进行复杂操作
def ConWithButton():
    return {"config": {"wide_screen_mode": True},
            "elements": [{"tag": "div","text": {"tag": "lark_md",
                                                "content": "点击下面的按钮上传发票。"},
                    "extra": {"tag": "button",
                              "text": {"tag": "lark_md","content": "上传发票"},
                              "type": "primary",
                              "url": "https://feishu.cn"}}]}
'''
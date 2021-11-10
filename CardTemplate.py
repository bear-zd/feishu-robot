

def ConWithPic(content, img_key="img_e344c476-1e58-4492-b40d-7dcffe9d6dfg", img_content='图片'):
    return {"config": {"wide_screen_mode": True},
            "elements": [{"tag": "div","text": {"tag": "lark_md",
                "content": content},
                "extra": {"tag": "img","img_key": img_key,
                "alt": {"tag": "plain_text","content": img_content}}}]}
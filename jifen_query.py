"""
获取积分,输入
"""
import json

import requests

from other.config_2 import index_url, post_url


def query_jifen(usrname,usrpass):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'Cookie': 'usrname={}; usrpwd={};'.format(usrname,usrpass),
        'Referer': index_url,
    }
    data = {
        'usrname': usrname,
        'usrpass': usrpass,
        'taskid': 'getwealth'

    }
    try:
        res=requests.post(url=post_url,data=data,headers=headers)
        jifen=json.loads(res.text)
        if jifen.get('wealth'):
            return jifen['wealth']
        else:
            return -1
    except:
        return None

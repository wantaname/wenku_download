'''百度短网址'''
import requests
import json

def toBaiduUrl(url):
    #请求地址
    request_url='https://dwz.cn/admin/v2/create'
    token="2f6929e5ac8480a988306360a9c06c46"
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Content-Type':'application/json',
        'Token':token,
    }
    data={
        'Url':url,
        'TermOfvalidity':'1-year',
    }

    reseponse=requests.post(url=request_url,data=json.dumps(data),headers=headers)
    res=reseponse.text#typ
    res=json.loads(res)
    print(res)
    if res.get('Code')==0:
        return res['ShortUrl']
    elif res.get('ErrMsg'):
        print(res['ErrMsg'])
    return url

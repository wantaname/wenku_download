import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config

#初始化浏览器，返回驱动对象
def init_chrome():
    # 初始化浏览器
    user_data_dir = r"--user-data-dir=" + config.wenku_user_data
    # 加载配置数据
    option = webdriver.ChromeOptions()
    option.add_argument('--log-level=3')
    option.add_argument('--safebrowsing-disable-download-protection')
    option.add_argument("--safebrowsing-disable-extension-blacklist")
    # option.add_argument('--headless')
    option.binary_location = config.brower_path
    prefs = {
        'download.default_directory': config.download_path,
        'safebrowsing.enabled': True,
    }
    option.add_experimental_option("prefs", prefs)
    option.add_argument(user_data_dir)
    option.add_argument('--disable-infobars')
    option.add_argument("--disable-notifications")
    # 浏览器驱动对象
    driver = webdriver.Chrome(chrome_options=option, executable_path=config.driver_path)
    return driver

#保证url无后缀
# def wenku_file_handle(url:str):
#     import zipfile
#
#     # 等待1秒
#     if not os.listdir(config.download_path):
#         time.sleep(2)
#     while True:
#
#
#         file_list = os.listdir(config.download_path)
#         if not file_list:
#             return None
#         if file_list[0].split(".")[-1] == "tmp":
#             continue
#         if file_list[0].find("crdownload") == -1:
#             # 文件全路径
#
#             print("下载完成")
#             break
#             # 在文件目录创建压缩文件
#     file = os.listdir(config.download_path)[0]
#     file_abs = os.path.join(config.download_path, file)
#     file_name=url.split('/')[-1]
#     zip_file = zipfile.ZipFile(os.path.join(config.wenku_path + file_name + '.zip'), "w", zipfile.ZIP_DEFLATED)
#     zip_file.write(file_abs, file)
#     zip_file.close()
#     # 删除文件
#     os.remove(file_abs)
#     url_path = "http://" + config.ip + "/" + config.dir + "/" + file_name + ".zip"
#     return url_path

#不要压缩
def wenku_file_handle(url:str):
    from baidu import toBaiduUrl
    # 等待1秒
    if not os.listdir(config.download_path):
        time.sleep(2)
    while True:


        file_list = os.listdir(config.download_path)
        if not file_list:
            return None
        if file_list[0].split(".")[-1] == "tmp":
            continue
        if file_list[0].find("crdownload") == -1:
            # 文件全路径

            print("下载完成")
            break

    #文件名
    file = os.listdir(config.download_path)[0]
    #文件路径
    file_abs = os.path.join(config.download_path, file)
    # 目标路径
    dest_abs=os.path.join(config.wenku_path, file)
    import shutil
    shutil.move(src=file_abs, dst=dest_abs)
    url_path = "http://" + config.ip + "/" + config.dir + "/" + file
    from urllib.parse import quote
    import string
    path=quote(url_path,safe=string.printable)
    print(path)
    short_path=toBaiduUrl(url=path)
    print(short_path)
    return short_path

#保证为标准url
def download(driver:webdriver.Chrome,url:str):

    print('初始化浏览器完成！')
    print("正在前往：" + url)
    driver.get(url)
    try:
        vip_btn = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "s-vip-text"))
        )
    except:
        return {'error': '账号未登录'}

    vip_btn = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'i.triangle-left + span'))
    )
    doc_types = driver.find_elements_by_css_selector('i.triangle-left + span')
    doc_type = ''
    for tt in doc_types:
        doc_type += tt.text
    doc_type=doc_type.strip()
    print(doc_type)

    if doc_type == "VIP专享文档":
        return {'type': 'private'}
    if doc_type == '共享文档':
        return {'type': 'public'}
    if doc_type == '付费文档':
        return {'type': 'pay'}
    if doc_type == "VIP免费文档":
        pass
    # 下载
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-download"))

        )
        btn = driver.find_element_by_class_name('btn-download')
        driver.execute_script("arguments[0].click();", btn)

    except:
        return {'error': 'click download btn error!'}

    try:
        confirm_ddl = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-diaolog-downdoc"))
        )
        confirm_ddl = driver.find_element_by_class_name("btn-diaolog-downdoc")
        confirm_ddl.click()
    except:
        #重复下载
        try:
            confirm_ddl = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='WkDialogOk']/b/b"))
            )
            confirm_ddl = driver.find_element_by_xpath("//*[@id='WkDialogOk']/b/b")
            confirm_ddl.click()
        except:
            return {'error': 'click confirm btn error!'}


    url_path = wenku_file_handle(url)
    # 下载成功会打开另一个窗口，需要关闭
    # 当前窗口句柄
    current_handle = driver.current_window_handle
    # 获取当前窗口句柄集合：列表
    handles = driver.window_handles
    for handle in handles:
        if handle != current_handle:
            driver.switch_to.window(handle)
            driver.close()
            driver.switch_to.window(current_handle)
    if url_path:
        return {'download_path': url_path}
    else:
        return {'error': 'vip文档下载失败!'}

#下载：专享和付费报错，
#url无后缀
def download_vip(driver:webdriver.Chrome,url:str,):
    print("正在前往："+url)
    driver.get(url)
    try:
        vip_btn = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "s-vip-text"))
        )
    except:
        return {'error':'账号未登录'}


    vip_btn = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'i.triangle-left + span'))
    )
    doc_types = driver.find_elements_by_css_selector('i.triangle-left + span')
    doc_type=''
    for tt in doc_types:
        doc_type+=tt.text
    print(doc_type)


    print(doc_type)
    if doc_type=="VIP专享文档":
        return {'type':'private'}
    if doc_type=='共享文档':
        return {'type':'public'}
    if doc_type=='付费文档':
        return {'type':'pay'}
    if doc_type=="VIP免费文档":
        pass
    #下载
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-download"))
            # EC.element_to_be_clickable((By.CLASS_NAME,'btn-download'))
        )
    except:
        return {'error':'get download btn error!'}
    btn=driver.find_element_by_class_name('btn-download')
    driver.execute_script("arguments[0].click();",btn)


    try:
        confirm_ddl=WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-diaolog-downdoc"))
            )
    except:
        return {'error':'click confirm btn error!'}
    confirm_ddl=driver.find_element_by_class_name("btn-diaolog-downdoc")
    confirm_ddl.click()
    url_path=wenku_file_handle(url)
    if url_path:
        return {'download_path':url_path}
    else:
        return {'error':'vip文档下载失败，请重试！'}

# def download_public(driver:webdriver.Chrome,url:str):
#     # 全局变量
#     server_url = "http://fen555.com/"
#     document_url = url
#     usrname = config.wenku_account
#     usrpass = config.wenku_password
#     # 等待首页加载成功
#
#
#     driver.get(server_url)
#     try:
#         element = WebDriverWait(driver, 6).until(
#             EC.presence_of_element_located((By.ID, "upbtn"))
#
#         )
#     except:
#
#         return {"error": "load page error!"}
#     # 输入账号密码等
#     element_url = driver.find_element_by_id('docid')
#     element_usrname = driver.find_element_by_id("baiduacc")
#     element_usrpass = driver.find_element_by_id("baidupwd")
#     element_ddl = driver.find_element_by_id('upbtn')
#
#     element_url.clear()
#     element_usrname.clear()
#     element_usrpass.clear()
#
#     element_url.send_keys(document_url)
#     element_usrname.send_keys(usrname)
#     element_usrpass.send_keys(usrpass)
#
#     element_ddl.click()
#     time.sleep(1)
#     driver.refresh()
#     try:
#         element_confirm = WebDriverWait(driver, 6).until(
#             EC.presence_of_element_located((By.ID, "upbtn"))
#         )
#     except:
#
#         return {"error":'click upbtn error!'}
#     element_confirm = driver.find_element_by_id("upbtn")
#     element_confirm.click()
#     # 不能下载的情况
#
#     # 下载成功
#     path = wenku_file_handle(document_url)
#     if path:
#
#         return path
#     else:
#         return {'error':'共享文档下载失败，请重试！'}
#下载共享文档，保证链接为标准链接
def download_public(url,usrname:str,usrpass:str):
    import requests
    import json

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'Cookie': 'usrname={}; usrpwd={};'.format(usrname,usrpass),
        'Referer': config.index_url,
    }
    data = {
        'usrname': usrname,
        'usrpass': usrpass,
        'docinfo': url,
        'taskid': 'up_down_doc1'

    }
    # 提交post
    res = requests.post(url=config.post_url, data=data, headers=headers)
    print(res.text)
    # 然后请求url
    dd = json.loads(res.text)


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'Cookie': 'usrname={}; usrpwd={};'.format(usrname,usrpass),
        'Referer': dd['url']
    }
    data = {
        'vid': dd['url'].split('id=')[-1],
        'taskid': 'directDown'
    }
    res = requests.post(url=config.index_url.rstrip('/') + '/downdoc.php', data=data, headers=headers)
    r = json.loads(res.text)
    print(r)

    if r['result'] == 'down_succ':
        print("下载成功！")

        url_id=url.split('/')[-1]
        from urllib.parse import quote, unquote
        import re
        file_url=unquote(r['dlink'].replace('%25', '%'))
        print(file_url)
        file_name=url_id

        pattern = 'filename(.)*?(\.)+([a-zA-Z])+'
        pos = re.search(pattern=pattern, string=file_url, flags=re.IGNORECASE)
        if pos:
            pos = pos.span()
            file_name = file_url[pos[0]:pos[1]]
            print(file_name)
            file_name = file_name.lstrip('filename').lstrip('*').lstrip('=').lstrip('"').lstrip('utf-8’’')
            print(file_name)
        ddl = requests.get(url=r['dlink'], headers=headers)
        with open(os.path.join(config.download_path, file_name), 'wb') as file:
            file.write(ddl.content)
        url_path = wenku_file_handle(url)
        if url_path:
            return {'download_path': url_path}
        else:
            return {'error': '共享文档下载失败，请重试！'}
    else:
        return {'error': '共享文档下载失败，请重试！'}



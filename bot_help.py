
from config import *
#数据库连接
import re
from datetime import datetime
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host=mail_host
mail_user=mail_user
mail_pass=mail_pass
mail_port=mail_port
sender=sender


class DatabaseConnect:
    # 类变量 无

    # 构造方法
    def __init__(self):
        # 实例变量
        self.host = database['host']
        self.port = database['port']
        self.user = database['user']
        self.password = database['password']
        self.database = database['database']
        self.charset = database['charset']
        # 连接对象
        self.conn = self.connect()
        # 游标对象
        self.cursor = self.cursor()

    # 连接
    def connect(self):
        conn = pymysql.connect(
            host=self.host, user=self.user, port=self.port,
            database=self.database, charset=self.charset, password=self.password)
        return conn

    # 关闭连接
    def close(self):
        self.conn.close()

    # 游标，字典
    def cursor(self):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cursor

    # 增
    def insert(self, sql) -> int:
        res = self.cursor.execute(sql)
        self.conn.commit()
        return res

    # 删除
    def delete(self, sql) -> int:
        """参数为要删除的条件"""
        res = self.cursor.execute(sql)
        self.conn.commit()
        return res

    # 查询一个
    def query_one(self, sql: str) -> dict:
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        self.conn.commit()
        return res

    # 查询所有
    def query_all(self, sql: str) -> list:
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        self.conn.commit()
        return res

    # 改
    def update(self, sql: str) -> int:
        res = self.cursor.execute(sql)
        self.conn.commit()
        return res


#处理消息类
class HandleMsg:

    def __init__(self,msg):
        self.origin_msg=msg
        self.msg=self.init_msg()#type:str

    def init_msg(self):
        #去掉@和首尾空格空行
        msg = self.origin_msg.replace("[CQ:at,qq=%d]" % (qqbot), '').strip()
        #去掉指令符
        msg=msg.lstrip('-')
        return msg

    def get_query_account(self):
        pattern = '查询积分(\s)*(\d)+(\s)+(\d)+'
        pos = re.search(pattern=pattern, string=self.msg)
        if pos:
            pos = pos.span()
            info = self.msg[pos[0]:pos[1]]
            info = info.replace('查询积分', '').strip()
            info=info.split()
            return {'usrname':info[0],'usrpass':info[1]}
        else:
            return None

    def get_leave_group(self):
        pattern='退群(\s)*(\d)+'
        pos = re.search(pattern=pattern, string=self.msg)
        if pos:
            pos = pos.span()
            info = self.msg[pos[0]:pos[1]]
            info=info.replace('退群','').strip()
            return int(info)
        else:
            return None
    #提取文库链接
    def get_wenku_url(self):
        pattern = '(http|https)://(wk|wenku)\.baidu\.com/view/[a-zA-Z0-9]+'
        pos = re.search(pattern=pattern, string=self.msg)
        if pos:
            pos = pos.span()
            url = self.msg[pos[0]:pos[1]]
            return url
        else:
            return None

    def get_email(self):
        pattern = "([a-zA-Z0-9]|_|-)+@([a-zA-Z0-9]|\.)+"
        pos = re.search(pattern=pattern, string=self.msg)
        if pos:
            pos=pos.span()
            mail = self.msg[pos[0]:pos[1]]
            return mail
        else:
            return None
    def get_chongzhi(self):
        pattern = '充值(\s)*wenku(\s)+(\d)+(\s)+(\d)+'
        pos = re.search(pattern=pattern, string=self.msg)
        if pos:
            pos = pos.span()
            msg = self.msg[pos[0]:pos[1]]
            msg = msg.replace('充值', '').replace('次', '').replace('wenku', '')
            info_list = msg.split()
            info = {'qq': info_list[0], 'count': int(info_list[1])}
            return info

    def is_chongzhi(self):
        if self.msg.strip()=='充值':
            return True
        else:
            return False

    def is_download(self):
        if self.msg.strip()=='下载':
            return True
        else:
            return False
    def is_query(self):
        if self.msg.strip()=='查询':
            return True
        else:
            return False

#查询用户剩余下载次数,返回下载次数
def query_wk_remain(user_id:str):
    conn = DatabaseConnect()
    # 查询用户
    sql = 'select * from wk_user WHERE qq="%s"' % (user_id,)
    res = conn.query_one(sql)
    # 如果没有查到用户，则添加
    if not res:
        # %s要加引号
        sql = 'INSERT into wk_user (qq,download_count,remain) VALUES ("%s",0,0)' % (user_id)
        conn.insert(sql=sql)

    # 查询用户剩余下载次数
    sql = 'select * from wk_user WHERE qq="%s"' % (user_id,)
    res=conn.query_one(sql)
    conn.close()
    return res['remain']

def direct_return(url):
    conn=DatabaseConnect()
    sql = 'select * from wk_download WHERE url="%s"' % (url,)
    res=conn.query_one(sql)
    conn.close()
    return res

def update_wk_user(user_id:str):

    conn = DatabaseConnect()

    sql = 'update wk_user set download_count=download_count+1,remain=remain-1 WHERE qq="%s"' % (user_id)
    conn.update(sql)

    conn.close()

def update_user_and_return(qq:str,url,download_path):
    conn = DatabaseConnect()
    sql = "update wk_user set download_count=download_count+1,remain=remain-1 WHERE qq='%s'"%(qq)
    res=conn.update(sql)
    sql = "insert into direct_return(url,download_path) VALUES ('%s','%s')"%(url, download_path)
    res = conn.insert(sql)
    conn.close()

def update_user_and_record(user_qq,url,download_path):
    conn = DatabaseConnect()
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = "update wk_user set download_count=download_count+1,remain=remain-1 WHERE qq='%s'"%(user_qq)
    res = conn.update(sql)
    #更新下载记录
    sql = "insert into wk_download(qq,url,download_path,download_time) VALUES ('%s','%s','%s','%s')" \
          ""%(user_qq, url ,download_path,time)
    res = conn.insert(sql)
    conn.close()

def send_remote_email(receivers,message):
    import socket
    import json
    host = "45.248.86.152"
    port = 1245
    s = socket.socket()
    s.connect((host, port))

    send_msg = [receivers, message]
    send_msg = json.dumps(send_msg)
    s.send(send_msg.encode('utf-8'))
    res = s.recv(4096).decode('utf-8')
    res = json.loads(res)  # type:bool
    s.close()
    return res


#传入发送者、接收者、msg
def send_email(receivers:list,msg:str,sender=sender)->bool:

    message=MIMEText(msg,_subtype='plain',_charset='utf-8')
    message["From"]=Header("发货机器人<%s>"%sender,'utf-8')
    message['To']=Header(receivers[0],'utf-8')

    subject="百度文库"
    message['Subject']=Header(subject,'utf-8')
    try:
        smtpObj=smtplib.SMTP_SSL(mail_host,port=mail_port)

        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender,receivers,message.as_string())
        return True
    except:
        return False


#返回剩余，同时写入充值记录
def wenku_chongzhi(qq:str,count:int):
    conn = DatabaseConnect()
    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "select * from wk_user WHERE qq='%s'" % (qq)
    res = conn.query_one(sql)
    if res:
        remain=res['remain']
    # 没有则新建用户
    else:
        sql = "insert into wk_user(qq,download_count,remain) VALUES ('%s',%d,%d)" % (qq, 0, 0)
        res = conn.insert(sql=sql)
        remain=0
    sql = "update wk_user set download_count=download_count,remain=remain+%d WHERE qq='%s'" % (count, qq)
    res = conn.update(sql)

    sql='insert into chongzhi(qq,count,time) VALUES ("%s",%d,"%s")'%(qq,count,time)
    res=conn.insert(sql)
    conn.close()
    return remain+count

def query_user(qq:str):
    conn = DatabaseConnect()
    sql = "select * from wk_user WHERE qq='%s'" % (qq)
    res = conn.query_one(sql)
    if res:
        conn.close()
        return res
    #新建用户
    else:
        sql = "insert into wk_user(qq,download_count,remain) VALUES ('%s',%d,%d)" % (
        qq, 0, 0)
        res = conn.insert(sql=sql)

    sql = "select * from wk_user WHERE qq='%s'" % (qq)
    res = conn.query_one(sql)
    conn.close()
    return res



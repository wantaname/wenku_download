from aiocqhttp import CQHttp

from bot_help import *
from download import download_public, download, init_chrome
from jifen_query import query_jifen
import config

bot=CQHttp(enable_http_post=False)
driver = init_chrome()

#群消息处理
@bot.on_message("group",)
async def handle_group_msg(context):

    #获取消息
    user_id = context['user_id']#type:int
    group_id = context['group_id']#type:int
    msg = context['message']  # type:str
    user_qq=str(user_id)
    #忽略其他群的消息
    if group_id not in config.group_id:
        return

    #消息对象
    msg=HandleMsg(msg)

    if user_id in config.super_id:
        query_account=msg.get_query_account()
        if query_account:
            jifen=query_jifen(usrname=query_account['usrname'],usrpass=query_account['usrpass'])

            if jifen:
                if jifen==-1:
                    return {'reply':'账号密码错误！'}
                else:
                    return {'reply':'剩余积分：{}'.format(jifen)}
            else:
                return {'reply':'查询失败！'}

    chongzhi = msg.get_chongzhi()
    if chongzhi and user_id in config.super_id:
        try:
            remain=wenku_chongzhi(qq=chongzhi['qq'], count=chongzhi['count'])
            reply='\n充值成功！'
            reply+="\n充值QQ：{}".format(chongzhi['qq'])
            reply+="\n充值次数：{}".format(chongzhi['count'])
            reply+='\n剩余次数：{}'.format(remain)

        except:
            reply="充值失败！"
        return {'reply':reply}



    if msg.is_chongzhi():
        return {'reply':'需要充值请联系管理员！'}

    if msg.is_download():
        return {'reply':'下载百度文库直接发链接即可！'}
    if msg.is_query():
        res=query_user(qq=user_qq)
        reply = "\n查询QQ：" + user_qq
        reply+='\n----------百度文库----------'
        reply+='\n已下载：{}次'.format(str(res['download_count']))
        reply+='\n剩余下载：{}次'.format(str(res['remain']))
        return {'reply':reply}


    url=msg.get_wenku_url()
    if not url:
        return
    # 数据库对象

    res=query_user(user_qq)
    if res['remain']<=0:
        reply  = '\n已下载：{}次'.format(str(res['download_count']))
        reply += '\n剩余下载：{}次'.format(str(res['remain']))
        reply +='\n-----------------------'
        reply +='\n下载次数不足，请联系管理员充值！'
        return {"reply": reply}

    await bot.send_group_msg(group_id=group_id, message="正在下载...")

    has_url=direct_return(url)
    if has_url:
        reply = "\n下载地址：" + has_url['download_path']
        # 更新账户
        # 更新用户次数和命中记录
        update_user_and_return(qq=user_qq, url=url, download_path=has_url['download_path'])

    else:
        ddl_path=None
        res=download(driver=driver,url=url)
        if res.get('error'):
            return {'reply':res['error']}

        elif res.get('download_path'):
            ddl_path = res['download_path']
        elif res.get('type'):
            if res['type']=='private':
                return {'reply':'此文档为专业文档，请联系管理员下载！'}
            if res['type']=='pay':
                return {'reply':'此文档为付费文档，请联系管理员下载！'}
            if res['type']=='public':
                import random
                account=random.choice(config.wenku_account)
                res_1=download_public(url=url,usrname=account[0],usrpass=account[1])

                if res_1.get('error'):
                    return {'reply': res_1['error']}

                else:
                    ddl_path=res_1['download_path']

        # 更新下载次数和记录
        update_user_and_record(user_qq=user_qq, url=url, download_path=ddl_path)
        reply='\n下载地址：'+ddl_path

    email=msg.get_email()
    #如果有邮箱
    if email:
        print(email)
        receivers=[email,]
        message= reply + config.ad_info
        res=send_email(receivers=receivers,msg=message)
        if res:
            reply += "\n邮件发送成功！"
        else:
            reply += "\n邮件发送失败！"
    return {'reply': reply}

#私聊消息处理
@bot.on_message("private",)
async def handle_private_msg(context):
    # 获取消息
    user_id = context['user_id']  # type:int
    msg = context['message']  # type:str
    user_qq = str(user_id)


    # 消息对象
    msg = HandleMsg(msg)

    if user_id in config.super_id:
        query_account=msg.get_query_account()
        if query_account:
            jifen=query_jifen(usrname=query_account['usrname'],usrpass=query_account['usrpass'])
            if jifen:
                if jifen==-1:
                    return {'reply':'账号密码错误！'}
                else:
                    return {'reply':'剩余积分：{}'.format(jifen)}
            else:
                return {'reply':'查询失败！'}

        if msg.msg=='功能介绍':
            reply='1.用户可以查询账户、下载文库'
            reply+='\n2.管理员可以给用户充值'
            reply+='\n3.支持发送到邮箱,链接和邮箱一起发即可，注意要可识别，不要连在一起！'
            return {'reply':reply}

        if msg.msg=='指令系统':
            reply='------特权指令------'
            reply+='\n1.功能介绍：-功能介绍'
            reply+='\n2.管理员充值：-充值 wenku QQ号 次数'
            reply+='\n---例：-充值 wenku 525817640 10次'
            reply+='\n3.退群指令：-退群 群号'
            reply+='\n4.查询文库账号积分：-查询积分 账号 密码'
            reply+='\n------用户指令------'
            reply+='\n5.下载：-下载'
            reply+='\n6.充值：-充值'
            reply+='\n7.查询：-查询'
            return {'reply':reply}


    #退群
    if user_id in config.super_id:
        leave_group=msg.get_leave_group()
        if leave_group:
            await bot.set_group_leave(group_id=leave_group)

    chongzhi = msg.get_chongzhi()
    if chongzhi and user_id in config.super_id:
        try:
            remain=wenku_chongzhi(qq=chongzhi['qq'], count=chongzhi['count'])
            reply='百度文库充值成功！'
            reply+="\n充值QQ：{}".format(chongzhi['qq'])
            reply+="\n充值次数：{}".format(chongzhi['count'])
            reply+='\n剩余次数：{}'.format(remain)
        except:
            reply="充值失败！"
        return {'reply':reply}

    if msg.is_chongzhi():
        return {'reply': '需要充值请联系管理员！'}

    if msg.is_download():
        return {'reply': '直接发链接即可！'}
    if msg.is_query():
        res = query_user(qq=user_qq)
        reply = "\n查询QQ：" + user_qq
        reply += '\n已下载：{}次'.format(str(res['download_count']))
        reply += '\n剩余下载：{}次'.format(str(res['remain']))
        return {'reply': reply}

    url = msg.get_wenku_url()
    if not url:
        return
    # 数据库对象

    res = query_user(user_qq)
    if res['remain'] <= 0:
        reply = '\n已下载：{}次'.format(str(res['download_count']))
        reply += '\n剩余下载：{}次'.format(str(res['remain']))
        reply += '\n-----------------------'
        reply += '\n下载次数不足，请联系管理员充值！'
        return {"reply": reply}

    await bot.send_private_msg(user_id=user_id, message="正在下载...")

    has_url = direct_return(url)
    if has_url:
        reply = "\n下载地址：" + has_url['download_path']
        # 更新账户
        # 更新用户次数和命中记录
        update_user_and_return(qq=user_qq, url=url, download_path=has_url['download_path'])



    else:

        ddl_path = None

        res = download(driver=driver, url=url)

        if res.get('error'):

            return {'reply': res['error']}


        elif res.get('download_path'):

            ddl_path = res['download_path']

        elif res.get('type'):

            if res['type'] == 'private':
                return {'reply': '此文档为专业文档，请联系管理员下载！'}

            if res['type'] == 'pay':
                return {'reply': '此文档为付费文档，请联系管理员下载！'}

            if res['type'] == 'public':

                import random

                account = random.choice(config.wenku_account)

                res_1 = download_public(url=url, usrname=account[0], usrpass=account[1])

                if res_1.get('error'):

                    return {'reply': res_1['error']}

                else:

                    ddl_path = res_1['download_path']

        # 更新下载次数和记录

        update_user_and_record(user_qq=user_qq, url=url, download_path=ddl_path)

        reply = '\n下载地址：' + ddl_path

    email = msg.get_email()
    # 如果有邮箱
    if email:
        receivers = [email, ]
        print(email)
        message = reply + config.ad_info
        res = send_email(receivers=receivers, msg=message)
        if res:
            reply += "\n邮件发送成功！"
        else:
            reply += "\n邮件发送失败！"
    return {'reply': reply}

#好友请求处理
@bot.on_request("friend")
async def hand_friend_request(context):
    # 将好友加到数据库
    conn = DatabaseConnect()

    user_id=str(context['user_id'])
    try:
        sql='insert into new_friend(qq) VALUES ("%s")'%(user_id)
        conn.insert(sql)
    except:
        print("添加好友到数据库失败！")
    # 建立账户
    sql = 'select * from wk_user WHERE qq="%s"' % (user_id,)
    res = conn.query_one(sql)
    # 如果没有查到用户，则添加
    if not res:
        # %s要加引号
        sql = 'INSERT into wk_user (qq,download_count,remain) VALUES ("%s",0,0)' % (user_id)
        conn.insert(sql)
    conn.close()
    return {'approve':True}

#加群请求处理
@bot.on_request('group')
async def handle_group_request(context):
    return {'approve':True}



# # 通知处理
# @bot.on_notice('group_increase')
# async def handle_group_increase(context):
#     message = '欢迎新人~你可以发送如下指令：'
#     message += "\n{}账户信息：-查询".format("[CQ:emoji,id=128147]")
#     message += "\n{}次数充值：-充值".format("[CQ:emoji,id=128147]")
#     message += '\n{}资源下载：-下载'.format("[CQ:emoji,id=128147]")
#     await bot.send(context, message=message,at_sender=True)

# 好友通知处理
@bot.on_notice('friend_add')
async def handle_friend_increase(context):
    message = '欢迎新人~你可以发送如下指令：'
    message += "\n{}账户信息：-查询".format("[CQ:emoji,id=128147]")
    message += "\n{}次数充值：-充值".format("[CQ:emoji,id=128147]")
    message += '\n{}资源下载：-下载'.format("[CQ:emoji,id=128147]")
    user_id=context['user_id']
    await bot.send_private_msg(user_id=user_id, message=message)

if __name__=="__main__":
    bot.run(host="127.0.0.1",port=8080)
"""
此为配置文件，所有目录统一“/”结尾
"""
#机器人所在QQ群
group_id=[]
#用于发广告的群
ad_group=
#超级管理员
super_id=[]

#机器人QQ号码,int
qqbot=



brower_path="C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
#chrome驱动路径
driver_path="./resource/chromedriver.exe"
dir="wenku"
#文件所在域名空间
ip=''
#下载路径,经测试只能用反斜杠！
download_path="C:\\Users\\Administrator\\Desktop\\wenku_download\\file_tmp"

#文库
wenku_path="./wenku/"

#数据库配置
database={
    "host":"",
    "port":3306,
    "user":"",
    "password":"",
    #必须要自己新建，表可以不用
    "database":"",
    "charset":"utf8",
}



index_url=''
post_url=''
wenku_account=[('',''),]
wenku_user_data='./wenku_user_data'

mail_host="smtp.qq.com"
mail_user=""
mail_pass=""
mail_port=465
sender=""

#邮箱中的广告信息
ad_info="""
这是机器人自动发的，你可以添加QQ群：，机器人在线自助下载!
"""
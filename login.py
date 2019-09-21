"""
登录
"""
from download import *

driver=init_chrome()

#前往登录
index_url="https://wenku.baidu.com/"




def login():
    driver.get(index_url)
    #判断是否登录
    try:
        login_btn = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "login"))
        )
        login_btn=driver.find_element_by_id('login')
        login_btn.click()
    except:
        # driver.quit()
        return "已登录"
    tip=input("登录成功按1：")
    if tip=="1":
        driver.quit()
        return "登录成功！"
    else:
        return "登录失败！"
print(login())




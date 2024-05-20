import json
import os
import time

import ddddocr
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

CONFIG_FILE = 'student.json'
"""
根据配置文件存在与否，获取并设置用户名和密码。
如果配置文件存在，则从文件中读取登录信息；
如果配置文件不存在或没有登录信息，则向用户索要登录信息。
"""
# 检查配置文件是否存在
if os.path.exists(CONFIG_FILE):
    # 配置文件存在，从文件中读取登录信息
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        # 检查数据中是否包含登录信息
        if 'login' in data:
            # 从读取的数据中获取用户名和密码
            USERNAME = data['login'][0]['username']
            PASSWORD = data['login'][0]['password']
        else:
            # 配置文件中没有登录信息，向用户索取
            USERNAME = input("请输入你的学号：")
            PASSWORD = input("请输入你的密码：")
else:
    # 配置文件不存在，向用户索取登录信息
    USERNAME = input("请输入你的学号：")
    PASSWORD = input("请输入你的密码：")
# 指定Edge驱动程序路径
service = webdriver.EdgeService(executable_path='MicrosoftWebDriver.exe')
# 启动Edge浏览器并最大化窗口
driver = webdriver.Edge(service=service)
driver.maximize_window()
# 打开登录页面
driver.get('https://sso.fvti.cn/login')
time.sleep(2)
# 查找并填写用户名
username = driver.find_element(By.NAME, 'username')
username.send_keys(USERNAME)
# 查找并填写密码
password = driver.find_element(By.XPATH, '//*[@id="login-normal"]/div[2]/form/div[2]/nz-input-group/input')
password.send_keys(PASSWORD)
# 查找验证码图片元素
code_img = driver.find_element(By.CLASS_NAME, 'code-img')
# 截取验证码图片的Base64编码
code_img_base64 = code_img.screenshot_as_base64
# 使用ddddocr识别验证码
ocr = ddddocr.DdddOcr(show_ad=False)
code_str = ocr.classification(code_img_base64)
# 查找验证码输入框，并通过模拟按键操作填写验证码
captcha_code = driver.find_element(By.NAME, 'captcha_code')
ActionChains(driver).send_keys(Keys.TAB).send_keys(code_str).perform()
# 点击登录按钮
login = driver.find_element(By.CLASS_NAME, 'login-button.ant-btn')
ActionChains(driver).click(login).perform()
# 点击教务系统学生端
time.sleep(1)
studentPortal = driver.find_element(By.XPATH, '//div[@class="buscarlist"]/ul/li[2]')
ActionChains(driver).click(studentPortal).perform()
print("已成功登录教务系统学生端")
time.sleep(3)
"""
指定课程表页面。
检查配置文件是否存在，如果存在则从文件中加载配置；如果不存在，则向用户询问配置信息。
"""
if os.path.exists(CONFIG_FILE):
    # 尝试从配置文件中读取学期配置
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        if 'kcb' in data:
            # 从文件中加载学期、学年、查询周次和专业代码
            xn = data['kcb'][0]['xn']
            xq = data['kcb'][0]['xq']
            dqz = data['kcb'][0]['dqz']
            sybmdmstr = data['kcb'][0]['sybmdmstr']
        else:
            # 配置文件中没有找到相应信息，提示用户输入
            xn = input("请输入查询学年（20XX-20XX）：")
            xq = input("请输入查询学期（1-2）：")
            dqz = input("请输入查询周次：")
            sybmdmstr = input("请输入查询专业代码（学号去掉后两位）：")
else:
    # 配置文件不存在，提示用户输入所有必要信息
    xn = input("请输入查询学年（20XX-20XX）：")
    xq = input("请输入查询学期（1-2）：")
    dqz = input("请输入查询周次：")
    sybmdmstr = input("请输入查询专业代码（学号去掉后两位）：")
# 构造访问的URL
url = 'https://10-1-1-100.webvpn.fvti.cn/studentportal.php/Jxxx/xskbxx/optype/2/xn/' + xn + '/xq/' + xq + '/dqz/' + dqz + '/sybmdmstr/' + sybmdmstr + '/'
# 打开构造的URL
driver.get(url)
# 切换到页面的主窗口
driver.switch_to.window(driver.window_handles[0])
# 提示用户检查内容是否正确
print("已成功打开课程表页面，若无内容请检查输入数据是否正确")
# 截图课程表
schedule_img = driver.find_element(By.CLASS_NAME, 'f4')
schedule_img.screenshot(xn + "_" + xq + "_" + dqz + "_" + sybmdmstr + '.png')
print("课程表已保存为“学年+学期+周次+专业代码.png”")
# 退出浏览器
driver.quit()
print("已自动退出")

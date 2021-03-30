import requests
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
import random
import json
import time
def check(text, browser):
    buttons = browser.find_elements_by_tag_name('button')
    for button in buttons:
        if button.get_attribute("textContent").find(text) >= 0:
            return True
    return False
def writeLog(text):
    with open('log.txt', 'a') as f:
        s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + text
        f.write(s + '\n')
        f.close()
def getUserData():
    try:
        with open("loginData.json", mode='r', encoding='utf-8') as f:
            loginData = f.readline()
            f.close()
    except FileNotFoundError:
        print("第一次使用需要提供一卡通号和密码，用于后续操作！")
        with open("loginData.json", mode='w', encoding='utf-8') as f:
            user = input('请输入一卡通账号： ')
            pw = input('请输入对应的密码： ')
            loginData = {"username": user, "password": pw}
            loginData = json.dumps(loginData) + '\n'
            f.write(loginData)
            f.close()
    return loginData

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('–no-sandbox')
chrome_options.add_argument('–disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_argument('--start-maximized')  # 最大化
chrome_options.add_argument('--incognito')  # 无痕隐身模式
chrome_options.add_argument("disable-cache")
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('--headless')

url = "https://newids.seu.edu.cn/authserver/login?service=http://ehall.seu.edu.cn/qljfwapp2/sys/lwReportEpidemicSeu/*default/index.do"

# get user data from loginData.json file
userData = getUserData()
loginData = json.loads(str(userData).strip())
user = loginData['username']
pw = loginData['password']

while True:
    try:
        browser = webdriver.Chrome(executable_path=r'./chromedriver',options=chrome_options)
        browser.get(url)
        browser.implicitly_wait(10)
        # fill username and password
        username = browser.find_element_by_id('username')
        password = browser.find_element_by_id('password')
        username.clear()
        password.clear()
        username.send_keys(user)
        password.send_keys(pw)

        # click login button
        login_button = browser.find_element_by_class_name('auth_login_btn')
        login_button.submit()
        browser.implicitly_wait(10)
        time.sleep(10)

        localtime = time.localtime(time.time())
        set_hour = 10
        set_minite = 0
        dailyDone = not check("新增", browser)

        if dailyDone is True and check("退出", browser) is True:  # Have finished report

            sleep_time = (set_hour+24-time.localtime(time.time()).tm_hour) * \
                3600 + (set_minite-time.localtime(time.time()).tm_min)*60
            writeLog("下次打卡时间：明天" + str(set_hour) + ':' +
                        str(set_minite) + "，" + "即" + str(sleep_time) + 's后')
            browser.quit()
            print("------------------浏览器已关闭----------------------")
            time.sleep(sleep_time)
        elif dailyDone is False:  # Haven't completed report
            buttons = browser.find_elements_by_css_selector('button')
            for button in buttons:
                if button.get_attribute("textContent").find("新增") >= 0:
                    button.click()
                    browser.implicitly_wait(10)

                    # temperature range 36.0-37.0
                    inputfileds = browser.find_elements_by_tag_name(
                        'input')
                    for i in inputfileds:
                        if i.get_attribute("placeholder").find("请输入当天晨检体温") >= 0:
                            i.click()
                            i.send_keys(str(random.randint(360, 370)/10.0))
                            buttons = browser.find_elements_by_tag_name(
                                            'button')
                            for button in buttons:
                                if button.get_attribute("textContent").find("确认并提交") >= 0:
                                    button.click()
                                    buttons = browser.find_elements_by_tag_name(
                                        'button')
                                    button = buttons[-1]

                                    # submit
                                    if button.get_attribute("textContent").find("确定") >= 0:
                                        button.click()
                                        dailyDone = True  # 标记已完成打卡
                                        writeLog("完成今日健康申报打卡成功！")
                                    else:
                                        print("WARNING: 学校可能改版，请及时更新脚本")
                                    break
                            break
                    break
            browser.quit()
            print("------------------浏览器已关闭----------------------")
            time.sleep(10)
        else:
            browser.close()
            writeLog("网络出现故障！")
            print("------------------网站出现故障----------------------")
            print("------------------浏览器已关闭----------------------")
            time.sleep(300)  # sleep 5min, in order to prevent network failure
    except Exception as r:
        print("未知错误 %s" % (r))
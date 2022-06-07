import os
import time

from appium import webdriver
#  ActivityRecord{cc14d7 u0 cn.amazon.mShop.android/com.amazon.mShop.navigation.MainActivity t1708}
#  packageName=cn.amazon.mShop.android processName=cn.amazon.mShop.android
#  taskAffinity=cn.amazon.mShop.android
#           realActivity=cn.amazon.mShop.android/com.amazon.mShop.splashscreen.StartupActivity
# 初始化参数
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

desired_caps = {
    'platformName': 'Android',  # 被测手机是安卓
    'platformVersion': '9',  # 手机安卓版本
    'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
    # 'appPackage': 'tv.danmaku.bili',  # 启动APP Package名称
    'appPackage': 'cn.amazon.mShop.android',  # 启动APP Package名称
    # 'appActivity': '.ui.splash.SplashActivity',  # 启动Activity名称
    'appActivity': 'com.amazon.mShop.splashscreen.StartupActivity',  # 启动Activity名称
    'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填True
    'resetKeyboard': True,  # 执行完程序恢复原来输入法
    'noReset': True,  # 不要重置App，如果为False的话，执行完脚本后，app的数据会清空，比如你原本登录了，执行完脚本后就退出登录了
    'newCommandTimeout': 6000,
    'automationName': 'UiAutomator2'
}
# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
time.sleep(5)


def getSize():
    size = driver.get_window_size()
    x = size['width']
    y = size['height']
    return (x, y)


def swipeUp():
    l = getSize()
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.75)
    y2 = int(l[1] * 0.25)
    driver.swipe(x1, y1, y2, 500)


def swipeDown():
    size = driver.get_window_size()
    x = size['width']
    y = size['height']
    ex = int(x * 0.5)
    ey = int(y * 0.2)
    sx = int(x * 0.5)
    sy = int(y * 0.6)
    # driver.swipe(x1, y1, y2, 500)
    driver.swipe(sx, sy, ex, ey)
    time.sleep(1)


asin = 'B09XRB52XJ'
sa = 'Sponsored Ad - '
listing = 'Wireless Microphone for iPhone iPad, Lavalier Wireless Lapel Microphone for Video Recording TikTok YouTube ' \
          'Live Stream, Plug-Play External Clip on Microphone for iPhone, No APP & Bluetooth Needed '
maxPage = 10
keywords = [
    # 'iphone mic',
    # 'video microphone',
    # 'mic for iphone',
    # 'bluetooth lavalier microphone',
    # 'wireless clip on microphone',
    # 'bluetooth lapel microphone',
    # 'lavalier microphone wireless',
    # 'small microphone',
    # 'mini microphone iphone',
    # 'lavalier mic',
    # 'clip on microphone wireless',
    # 'bluetooth wireless microphone',
    # 'bluetooth microphone',
    # 'ipad microphone',
    # 'mini microphone wireless',
    # 'wireless microphone for iphone',
    # 'mic for iphone video recording',
    # 'lapel microphone',
    # 'wireless lavalier microphones & systems',
    # 'wireless mic for iphone',
    # 'wireless lavalier microphone',
    # 'wireless microphone',
    # 'wireless lavalier microphone for iphone',
    'youtube microphone for recording videos',
    'iphone microphone for video recording',
    'wireless microphones',
    'microphone',
    'wireless microphone for iphone',
    'iphone wireless microphone',
    'wireless mic for iphone',
    'iphone microphone',
    'lapel microphone',
    'iphone microphone for video recording',
    'microphone for iphone video recording',
    'bluetooth microphone for iphone',
    'lapel microphone iphone',
    'wireless bluetooth microphone',
    'iphone external microphone',
    'iphone microphone for recording',
    'microphone for iphone',
    'wireless microphones',

]

# 退出程序，记得之前没敲这段报了一个错误 Error: socket hang up 啥啥啥的忘记了，有兴趣可以try one try
searchInputElement = driver.find_element(by=By.ID, value="cn.amazon.mShop.android:id/chrome_search_hint_view")
for keyword in keywords:
    productName = set()
    searchInputElement.click()
    searchInput = driver.find_element(by=By.ID, value='cn.amazon.mShop.android:id/rs_search_src_text')
    searchButton = driver.find_element(By.ID, 'cn.amazon.mShop.android:id/chrome_action_bar_search_icon')
    searchInput.send_keys(keyword)
    os.system('adb shell ime set com.sohu.inputmethod.sogou/.SogouIME')
    time.sleep(1)
    driver.press_keycode(66)
    time.sleep(5)
    # 此关键词所有页面
    pageNow = 1  # 当前页
    while pageNow < maxPage:
        ranking = 0
        # 当前页遍历
        while True:
            try:
                video = driver.find_element(By.CSS_SELECTOR, '[content-desc=Sponsored video*]')
                video.__setattr__('displayed', False)
            except:
                print('没有视频元素')
            productImages = driver.find_elements(By.CLASS_NAME, 'android.widget.Image')
            for productImage in productImages:
                text = productImage.get_attribute("text")
                if text == '' or text == 'Prime Eligible' or text == 'Eligible for Prime.' or text == 'Amazon Prime' or len(
                        text) < 20:
                    continue
                if text not in productName:
                    productName.add(text)
                    ranking = ranking + 1
                    # img = productImage.screenshot('E:\\bbsearch\\' + keyword.replace(" ", '') + "_" + text + ".png")
                    # print("产品名字：" + text)
                    # print("当前遍历位置：", ranking)
                    if listing.__contains__(text.replace(sa, '').replace('...', '')):
                        if text.__contains__(sa):
                            print("找到产品广告位置：" + keyword, "当前页：", pageNow, '页内排名', ranking)
                        else:
                            print("找到产品自然位置：" + keyword, "当前页：", pageNow, '页内排名', ranking)
            try:
                nextPage = driver.find_element(By.XPATH, '//android.view.View[@content-desc="Next→"]')
                nextPage.click()
                time.sleep(3)
                break
            except:
                swipeDown()
        pageNow = pageNow + 1
driver.quit()

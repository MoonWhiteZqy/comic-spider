from selenium import webdriver
import json, time

url = 'https://www.baidu.com/'
browser = webdriver.Chrome()
def get_cookie():
    browser.get(url)
    time.sleep(40)
    with open('cookie.txt','w') as f:
        f.write(json.dumps(browser.get_cookies()))
    browser.close()
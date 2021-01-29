from selenium import webdriver
import json, time

if __name__ == '__main__':
    url = 'https://www.u17.com/comic/76564.html'
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(40)
    with open('cookie.txt','w') as f:
        f.write(json.dumps(browser.get_cookies()))
    browser.close()
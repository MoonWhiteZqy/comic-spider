from selenium import webdriver
import time
import json
import requests
from bs4 import BeautifulSoup
import re
import os

option = webdriver.ChromeOptions()
option.add_argument('headless')


def download_img(url, index, folder):
    # 进入漫画页面，通过cookie模拟登陆操作
    try:
        browser = webdriver.Chrome(options=option)
        browser.get(url)
        browser.delete_all_cookies()
        with open('cookie.txt', 'r') as f:
            cookie_list = json.load(f)
            for cookie in cookie_list:
                browser.add_cookie(cookie)
        time.sleep(2)
        browser.refresh()
    except:
        print('网页打开失败')
        if not os.path.exists(folder):
            os.mkdir(folder)
        files = os.listdir(folder)
        file_index = len(files) + 1
        file_name = file_index.__str__() + '.jpg'
        real_name = folder + '/' + file_name
        img = b'1111'
        with open(real_name, 'wb') as f:
            f.write(img)
        print(real_name + '下载失败')
        return
    source = browser.page_source
    source = BeautifulSoup(source, features='html.parser')

    # 漫画图片的地址
    img_url = source.find('img', {'id': 'cur_img_' + index})
    if not os.path.exists(folder):
        os.mkdir(folder)
    files = os.listdir(folder)
    file_index = len(files) + 1
    file_name = file_index.__str__() + '.jpg'
    real_name = folder + '/' + file_name
    try:
        img = requests.get(img_url['src']).content
    except:
        img = b'1111'
    with open(real_name, 'wb') as f:
        f.write(img)
    print(real_name + '下载完成')
    browser.close()


def load_cookie(browser, url, chapter_name, path):
    browser.get(url)
    browser.delete_all_cookies()
    with open('cookie.txt', 'r') as f:
        cookie_list = json.load(f)
        for cookie in cookie_list:
            browser.add_cookie(cookie)
    browser.refresh()
    time.sleep(1)
    # 当前章节的基础url
    base_url = url + '#image_id='

    source = browser.page_source
    pattern = r'image_list:.*\n.*image_page'
    source = re.findall(pattern, source)[0]
    source = source[source.index(' ') + 1:source.index('}}') + 2]
    image_list = json.loads(source)
    browser.close()

    print('开始进行下载，当前章节：' + chapter_name)
    for key, value in image_list.items():
        image_id = value['image_id']
        download_img(base_url + image_id, image_id, path + chapter_name)
    print(chapter_name + '下载结束')


# 给定漫画的目录页面url，获得各个章节首页的url，传入保存的文件夹路径
def get_links(url, path):
    page = requests.get(url).text
    links = BeautifulSoup(page, features='html.parser').find_all('a', {'id': re.compile('cpt_[0-9]+')})
    index = 0
    for link in links:
        print(link['href'])
        print(link['title'])
        index += 1
        if index <= len(os.listdir(path)):
            continue
        try_time = 0
        for try_time in range(5):
            try:
                browser = webdriver.Chrome(options=option)
                break
            except:
                pass
        if try_time == 4:
            os.mkdir(path + link['title'].rstrip())
            print('漫画开头页访问失败')
        else:
            load_cookie(browser, link['href'], link['title'].rstrip(), path)


if __name__ == '__main__':
    folder_path = 'D:/文件/漫画/镇魂街/'
    web_link = 'https://www.u17.com/comic/3166.html'
    get_links(web_link, folder_path)

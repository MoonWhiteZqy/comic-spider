from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import json
import requests
from bs4 import BeautifulSoup
import re
import os

option = webdriver.ChromeOptions()
option.add_argument('headless')
global cookie_list

def read_cookie():
    with open('cookie.txt', 'r') as f:
        global cookie_list
        cookie_list = json.load(f)


def load_cookie(browser):
    global cookie_list
    browser.delete_all_cookies()
    for cookie in cookie_list:
        browser.add_cookie(cookie)


def download_img(url, index, file_name):
    view_fail = True
    img = b'1111'
    # 进入漫画页面，通过cookie模拟登陆操作
    for i in range(4):
        try:
            browser = webdriver.Chrome(options=option)
            browser.get(url)
            load_cookie(browser)
            # time.sleep(2)
            browser.refresh()
            view_fail = False
            break
        except:
            continue
    if view_fail:
        print('页面打开失败')
        print(file_name + '下载失败')
        return
    source = browser.page_source
    source = BeautifulSoup(source, features='html.parser')

    # 获取漫画图片的地址
    img_url = source.find('img', {'id': 'cur_img_' + index})
    try:
        img = requests.get(img_url['src']).content
    except:
        print('未知错误')
        pass
    with open(file_name, 'wb') as f:
        f.write(img)
    print(file_name + '下载完成')
    browser.quit()


# 开始下载漫画
def download_comic(url, chapter_name, path):
    # 检查下载路径
    folder = path + chapter_name
    if not os.path.exists(folder):
        os.mkdir(folder)
    # 用于判断是否访问成功
    view_fail = True
    for i in range(4):
        try:
            browser = webdriver.Chrome(options=option)
            browser.get(url)
            load_cookie(browser)
            browser.refresh()
            view_fail = False
            break
        except WebDriverException:
            continue
        except:
            print('未知错误')
            continue

    if view_fail:
        print(chapter_name + '访问失败')
        return
    # time.sleep(2)
    # 当前章节的基础url
    base_url = url + '#image_id='

    source = browser.page_source
    # 通过正则表达式找到记录图片id的json字符串
    pattern = r'image_list:.*}}'
    source = re.findall(pattern, source)[0]
    # 删除前缀，只留下数据的json字符串
    source = source[source.index(' ') + 1:]
    image_list = json.loads(source)
    browser.quit()

    print('开始进行下载，当前章节：' + chapter_name)
    for key, value in image_list.items():
        image_id = value['image_id']
        file_name = folder + '/' + key + '.jpg'
        if os.path.exists(file_name):
            continue
        download_img(base_url + image_id, image_id, file_name)
    print(chapter_name + '下载结束')


def get_comic_by_links(links, path):
    # 首先检查存储路径是否存在，若不存在，则创建
    if not os.path.exists(path):
        try:
            os.mkdir(path)
            print('路径不存在，已创建')
        except FileNotFoundError:
            print('不存在父目录，创建失败')
            exit(0)
    # 根据路径下的文件夹判断下载进度
    index = 0
    for link in links:
        print('当前链接:' + link['href'])
        print('当前章节:' + link['title'])
        index += 1
        # 检验到章节已下载，跳过
        if index < len(os.listdir(path)):
            continue
        # 进入漫画开头页
        download_comic(link['href'], link['title'].rstrip(), path)


# 给定漫画的目录页面url，获得各个章节首页的url，传入保存的文件夹路径
def get_links(url):
    page = requests.get(url).text
    links = BeautifulSoup(page, features='html.parser').find_all('a', {'id': re.compile('cpt_[0-9]+')})
    return links


if __name__ == '__main__':
    folder_path = 'D:/文件/漫画/星迹/'
    web_link = 'https://www.u17.com/comic/76564.html'
    comic_links = get_links(web_link)
    read_cookie()
    get_comic_by_links(comic_links, folder_path)

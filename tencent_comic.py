from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
import time

base_url = 'https://ac.qq.com'
base_folder = 'D:/文件/漫画/我机器人/'
option = webdriver.ChromeOptions()
option.add_argument('headless')

def get_chapter_links(web_url):
    res = []
    page = requests.get(web_url).text
    links = BeautifulSoup(page, features='html.parser').find_all('ol', {'class':"chapter-page-all"})[0].find_all('a')
    for link in links:
        res.append({
            'href':link['href'],
            'title':link.text.replace('\r\n', '').strip()
        })
    return res


def download_img(infos):
    for i in range(len(infos)):
        info = infos[i]
        if i <= 247:
            continue
        url = base_url + info['href']
        title = info['title']
        title = title.replace('\\', '')
        title = title.replace('\/', '')
        title = title.replace('?', '')
        print('当前章节:' + title)
        print('当前序号:' + i.__str__())
        path = base_folder + title + '/'
        if not os.path.exists(path):
            os.mkdir(path)
        browser = webdriver.Chrome(options=option)
        browser.get(url)
        # 切换成翻页模式
        sw_btn = browser.find_element_by_class_name('icon-dpage')
        sw_btn.click()
        # right_btn = browser.find_element_by_class_name('page-arrow-right')
        # page_num = browser.find_element_by_id('toolPageNow').text
        # page_num = page_num.split('/')[1]
        # num_range = int(page_num) - 1
        # for i in range(num_range):
        #     time.sleep(2)
        #     picture = browser.find_element_by_class_name('pic-with-roast').img
        #     print(picture)
        #     right_btn.click()
        source = browser.page_source
        source = BeautifulSoup(source, features='html.parser').find_all('div', {'class':'pic-with-roast'})
        count = 0
        for div in source:
            count += 1
            file_name = count.__str__() + '.jpg'
            img_tag = div.img
            try:
                img_url = img_tag['src']
            except:
                img_url = img_tag['data-src']
            if os.path.exists(path + file_name):
                continue
            try:
                img = requests.get(img_url).content
            except:
                img = b'1111'
            with open(path + file_name, 'wb') as f:
                f.write(img)
            print(path + file_name + '下载完成')
        print('-----------------------------------')
        browser.quit()

if __name__ == '__main__':
    web_url = "https://ac.qq.com/Comic/ComicInfo/id/622861"
    links = get_chapter_links(web_url)
    download_img(links)
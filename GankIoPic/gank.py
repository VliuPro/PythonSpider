# coding: utf-8

import re
import threading
from queue import Queue

import requests
from bs4 import BeautifulSoup

url_queue = Queue()
PATH = '/home/vliupro/sourses/pic/gankio/'


class GankIo:
    def __init__(self):
        self.URL = 'http://gank.io/history'

    def makeUrl(self):
        urls = []
        base = 'http://gank.io'
        page = requests.get(self.URL)
        bs = BeautifulSoup(page.content, 'lxml')
        a_list = bs.find_all('div', class_='content')[0].select('ul li div a')
        for a in a_list:
            url = a['href']
            urls.append(base + url)
        return urls


class GankThread(threading.Thread):
    def __init__(self, url_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue

    def getPage(self, url):
        page = requests.get(url)
        return page.content

    def getImgUrl(self, page):
        imgurls = []
        bs = BeautifulSoup(page, "lxml")
        img = bs.find_all(src=re.compile('http://.*?sinaimg.*?large.*?jpg.*?'))
        for i in img:
            imgurls.append(i['src'])
        return imgurls

    def saveImg(self, img, name):
        print("download: " + name)
        with open(PATH + name, 'wb') as f:
            f.write(img)
            f.close()

    def run(self):
        while True:
            url = self.url_queue.get()
            page = self.getPage(url=url)
            imgUrls = self.getImgUrl(page=page)
            for imgUrl in imgUrls:
                img = self.getPage(url=imgUrl)
                name = imgUrl.split('/')[-1]
                self.saveImg(img, name)
            self.url_queue.task_done()


if __name__ == '__main__':
    gank = GankIo()
    urlList = gank.makeUrl()
    print("长度： " + str(len(urlList)))
    for url in urlList:
        url_queue.put(url)

    for i in range(4):
        t = GankThread(url_queue)
        t.setDaemon(True)
        t.start()

    url_queue.join()

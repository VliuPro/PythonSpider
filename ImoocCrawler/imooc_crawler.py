#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import requests
from bs4 import BeautifulSoup


class ImoocCrawler:

    name = 'imooc'
    # 具体课程的前缀，后面加上课程代码,用来获取具体video的后缀代码
    learn_prev = 'http://www.imooc.com/learn/{}'
    # 获取video地址的url前缀，后面加上具体video的后缀代码
    info_prev_url = 'http://www.imooc.com/course/ajaxmediainfo/?mid={}'
    # 默认保存路径
    base_dir = os.path.split(os.path.realpath(__file__))[0]

    def __init__(self, learn_id):
        self.learn_id = learn_id
        self.video_ids = []
        self.video_urls = []

    def getResponse(self, url):
        return requests.get(url)

    def parser_video_id(self, response, url):
        result = {}
        if response == None:
            print('获取数据失败, ' + str(url))
            return None
        else:
            bs = BeautifulSoup(response.content, 'lxml')
            # 获取该页标题
            result['title'] = bs.find_all("div", class_="hd")[0].select('h2')[0].string
            # 获取该页的所有video的id
            for video_li in bs.find_all('ul', class_='video'):
                for video_a in video_li.select('a'):
                    self.video_ids.append(video_a.get('href').split('/')[2])
                    print("添加video的ID：" + video_a.get('href').split('/')[2])

    def parser_video_url(self, response, url):
        if response == None:
            print('获取JSON数据失败，' + str(url))
            return None
        else:
            url_json = response.json()
            self.video_urls.append((url_json['data']['result']['name'],
                                    url_json['data']['result']['mpath'][1]))
            print("添加video地址和名称：url = " + url_json['data']['result']['mpath'][1] + ", name = "
                  + url_json['data']['result']['name'])

    def download_video(self):
        target_dir = os.path.join(self.base_dir, 'imooc')
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        os.chdir(target_dir)
        for video_url in self.video_urls:
            response = requests.get(video_url[1], stream=True)
            with open(video_url[0] + '.mp4', 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            print(video_url[0] + '.mp4 --- 下载完成')

    def start(self):
        real_learn_url = self.learn_prev.format(self.learn_id)
        # 获取课程主页的信息，并将主页列表中video的id存起来
        print("获取video的id列表... url = " + real_learn_url)
        self.parser_video_id(self.getResponse(real_learn_url), real_learn_url)
        for video_id in self.video_ids:
            real_video_url = self.info_prev_url.format(video_id)
            # 解析JSON获取video真实地址
            self.parser_video_url(self.getResponse(real_video_url), real_video_url)
        self.download_video()


def check_id(id_str):
    ids = id_str.split(',')
    for id in ids:
        try:
            int(id.strip())
        except:
            print('输入错误, ' + id.strip())
            exit(0)


if __name__ == '__main__':
    learn_id = input("请输入课程代码（以','间隔）：").strip()
    check_id(learn_id)
    learn_ids = learn_id.split(',')
    # print(learn_ids)
    # print('dir is : ' + os.path.split(os.path.realpath(__file__))[0])
    for learnid in learn_ids:
        imooc = ImoocCrawler(learnid)
        imooc.start()

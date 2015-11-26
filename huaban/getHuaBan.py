#!/usr/bin/env python
# coding: utf-8

import requests
import re
import os

class Huaban:
    imgPre = 'http://img.hb.aicdn.com/'

    def __init__(self,index):
        self.index = index
        print(self.index)

    def getResponse(self):
        response = requests.get(self.index)
        return response

    def getKeyList(self):
        pattern_sc = re.compile(r'<script>(.*?)</script>',re.S)
        sc_list = re.findall(pattern_sc,self.getResponse().text)
        pattern_key = re.compile(r'"key"\:.*?"(.*?)".*?,',re.S)
        key_list = re.findall(pattern_key,sc_list[1])
        return key_list

    def getImgContent(self,imgUrl):
        img = requests.get(imgUrl)
        return img.content


    def downloadImg(self):
        key_list = self.getKeyList()
        if not os.path.exists('./pic/'):
            os.mkdir('./pic/')
        i = 0
        for key in key_list[:-6]:
            imgUrl = self.imgPre + key + '_fw658'
            imgcon = self.getImgContent(imgUrl)
            if (imgcon):
                print('Downloading pic %s , file name is %s' % (key,str(i)))
                f = open('./pic/%s.jpg' % (str(i)), 'wb')
                i += 1
                f.write(imgcon)


if __name__ == '__main__':
    url = input('请输入：')
    img = Huaban(url)
    img.downloadImg()

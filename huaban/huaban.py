#!/usr/bin/env python
# coding: utf-8

import requests
import re

class Huaban:
    imgPre = 'http://img.hb.aicdn.com/'
    path = './pic/'
    def __init__(self,index,max_img):
        self.max_img = max_img
        self.index = index

    def getResponse(self,max_img):
        headers = { "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36" }
        group_url = '%s?page=1&per_page=%s&wfl=1' % (self.index,max_img)
        print(group_url)
        response = requests.get(group_url,headers = headers)
        return response

    def getGroups(self,max_img):
        response = self.getResponse(max_img)
        reg = re.compile(r'"pin_id":(\d+),.*?"file":{.*?"key":"(.*?)".*?"type":"image/(.*?)"',re.S)
        return re.findall(reg,response.text)

    def downLoadImg(self,groups):
        print(groups)
        if groups:
            for attr in groups:
                pin_id = attr[0]
                attr_url = attr[1] + '_fw658'
                img_type = attr[2]
                img_url = 'http://img.hb.aicdn.com/' + attr_url
                filepath = self.path + pin_id + '.' + img_type
                r = requests.get(img_url)
                print('download img %s' % filepath)
                with open(filepath,'wb') as fd:
                    fd.write(r.content)

    def run(self):
        while True:
            groups = self.getGroups(self.max_img)
            if not groups:
                break
            else:
                self.downLoadImg(groups)

if __name__ == '__main__':
    url = input('网址：')
    max_img = input('数量：')
    img = Huaban(url,max_img)
    img.run()

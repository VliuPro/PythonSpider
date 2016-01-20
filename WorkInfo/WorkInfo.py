# coding:utf-8
__author__ = 'vliupro'

import requests
import json


class Lagou:
    def __init__(self):
        self.__form_data = {}
        self.__url = 'http://www.lagou.com/jobs/positionAjax.json?'
        self.__headers = {}
        self.cookies = requests.get('http://www.lagou.com').cookies

    def getPageJson(self, key_word, page):
        self.__makeData(key_word, page)
        return requests.post(self.__url, data=self.__form_data, headers=self.__headers).json()

    def __makeData(self, key_word, page):
        self.__url = self.__url + 'px=default&first=' + (page == 1 and 'true' or 'false') + '&kd=' + key_word + '&pn=' + page
        form_data = {'first': page == 1 and 'true' or 'false',
                     'pn': page,
                     'kd': key_word}
        self.__form_data = json.dumps(form_data)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'Host': 'www.lagou.com',
            'Cookie' : ';'.join(['='.join(item) for item in self.cookies.items()])}
        self.__headers = headers


class Page:
    def __init__(self, key_word, page_no):
        self.__key_word = key_word
        self.__page_no = page_no
        self.current_page = 0
        self.has_next = False
        self.has_prev = False
        self.page_size = 0
        self.total_count = 0
        self.total_page = 0
        self.jobs = []

    def setPage(self):
        lagou = Lagou()
        json_data = lagou.getPageJson(self.__key_word, self.__page_no)['content']
        self.current_page = int(str(json_data['currentPageNo']))
        self.has_next = json_data['hasNextPage'] == str('true')
        self.has_prev = json_data['hasPreviousPage'] == str('false')
        self.page_size = json_data['pageSize']
        self.total_count = json_data['totalCount']
        self.total_page = json_data['totalPageCount']
        result = json_data['result']
        # print(result)
        for r in result:
            # print(r['positionName'])
            self.jobs.append(Job(r))

class Job:
    def __init__(self, jd):
        self.position_name = jd['positionName']
        self.position_type = jd['positionType']
        self.salary = jd['salary']
        self.education = jd['education']
        self.workyear = jd['workYear']
        self.city = jd['city']
        self.company_name = jd['companyName']
        self.company_short_name = jd['companyShortName']
        self.company_stage = jd['financeStage']
        self.company_field = jd['industryField']
        self.company_size = jd['companySize']
        self.company_labellist = jd['companyLabelList']
        self.job_nature = jd['jobNature']
        self.position_advantage = jd['positionAdvantage']
        self.position_type = jd['positionFirstType']
        self.create_time = jd['createTime']


if __name__ == '__main__':
    key = input("请输入关键词：")
    pageno = input("请输入页：")
    page = Page(key,pageno)
    page.setPage()

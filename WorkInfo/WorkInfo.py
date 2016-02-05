# coding:utf-8
__author__ = 'vliupro'

import json

import pymysql
import requests


class Lagou:
    def __init__(self):
        self.__form_data = {}
        self.__url = 'http://www.lagou.com/jobs/positionAjax.json?'
        self.__headers = {}
        self.cookies = requests.get('http://www.lagou.com').cookies
        self.pn = 1

    def getPageJson(self, key_word):
        self.__makeData(key_word, self.pn)
        return requests.post(self.__url, data=self.__form_data, headers=self.__headers).json()

    def __makeData(self, key_word, page):
        self.__url = self.__url + 'px=default&first=' + (
            page == 1 and 'true' or 'false') + '&kd=' + key_word + '&pn=' + str(page)
        form_data = {'first': page == 1 and 'true' or 'false',
                     'pn': page,
                     'kd': key_word}
        self.__form_data = json.dumps(form_data)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'Host': 'www.lagou.com',
            'Cookie': ';'.join(['='.join(item) for item in self.cookies.items()])}
        self.__headers = headers


class Page:
    def __init__(self, key_word):
        self.__key_word = key_word
        self.__page_no = 0
        self.current_page = 0
        self.has_next = False
        self.has_prev = False
        self.page_size = 0
        self.total_count = 0
        self.total_page = 0
        self.jobs = []

    def setPage(self, lagou):
        self.__page_no = lagou.pn
        json_data = lagou.getPageJson(self.__key_word)['content']
        self.current_page = int(str(json_data['currentPageNo']))
        self.has_next = json_data['hasNextPage'] == str('true')
        self.has_prev = json_data['hasPreviousPage'] == str('false')
        self.page_size = json_data['pageSize']
        self.total_count = json_data['totalCount']
        self.total_page = json_data['totalPageCount']
        result = json_data['result']
        # print(result)
        for r in result:
            # print(str(r['positionId']))
            self.jobs.append(Job(r))


class Job:
    def __init__(self, jd):
        # print(type(jd))
        self.position_Id = str(jd['positionId'])
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
        self.position_first_type = jd['positionFirstType']
        self.create_time = jd['createTime']
        self.__saveIntoMysql()

    def __saveIntoMysql(self):
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='vliupro', passwd='liujida', db='offertest')
        conn.set_charset('utf8')
        cur = conn.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        savesql = str(r'insert into db_jobs(positionId,positionName,positionType,salary,education,workYear,city,companySName,companyName,companyStage,companyField,companySize,companyLabellist,nature,positionAdvantage,positionFType,createTime) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            self.position_Id, self.position_name, self.position_type, self.salary, self.education, self.workyear,
            self.city,
            self.company_short_name, self.company_name, self.company_stage, self.company_field, self.company_size, (
                ','.join(
                    self.company_labellist)), self.job_nature, self.position_advantage, self.position_first_type,
            self.create_time)).encode(encoding='utf-8')
        print(savesql)
        # try:
        cur.execute(savesql)
        conn.commit()
        # except Exception:
        #     print('插入错误')
        cur.close()
        conn.close()

if __name__ == '__main__':
    key = input("请输入关键词：")
    lagou = Lagou()
    page = Page(key)
    page.setPage(lagou)
    if page.has_next == 'true':
        lagou.pn += 1
        page.setPage()
    # print(type(page.jobs[0]))
    # print(','.join(page.jobs[0].company_labellist))

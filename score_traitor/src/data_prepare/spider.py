import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from requests.cookies import RequestsCookieJar
import json
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from multiprocessing.dummy import Pool as ThreadPool
import itertools

PATH_UNIVERSITY = '/Users/kunyue/project_personal/my_project/score_traitor/data/data_spider/'


def get_cookie(username, password):
    pass
    chromedriver = '/Users/kunyue/project_personal/my_project/score_traitor/resource/chromedriver-1'
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://www.wmzy.com/')  # JD 登录页面
    time.sleep(2)  # 等待加载
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.LINK_TEXT, "快速登录"))
    )
    driver.find_element_by_link_text('快速登录').click()  # 切换登录按钮
    time.sleep(2)
    driver.find_element_by_name('mobile').send_keys(username)  # 填写账号
    driver.find_element_by_name('password').send_keys(password)  # 填写密码
    driver.find_element_by_xpath('//button[text()="登录"]').click()  # 点击登录按钮
    driver.delete_all_cookies()
    time.sleep(15)  # 等待加载
    jd_cookies = driver.get_cookies()
    driver.close()  # 关闭浏览器
    pickle.dump(jd_cookies, open('cookies.pkl', 'wb'))  # 保存cookies
    # print('cookies save successfully!')


def download_score_index_page(url):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    print(cookies)
    cookie_jar = RequestsCookieJar()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    print(soup)
    print(soup.getText())


# //列表页
def download_page_university(url, page_num):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    print(cookies)
    newHeaders = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Channel': 'www.wmzy.com pc',
        'Connection': 'keep-alive',
        'Content-Length': '37',
        'Content-Type': 'application/json',
        'Host': 'www.wmzy.com',
        'Origin': 'https://www.wmzy.com',
        'Referer': 'https://www.wmzy.com/web/school/list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 x-requested-with: XMLHttpRequest}'}
    cookie_jar = RequestsCookieJar()
    payload = {"filter": {}, "page": page_num, "page_size": 20}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.post(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    result = site_json['data']['sch_short_info']
    print('进度：:', page_num)
    return result


def download_page_index(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    # kargs['university_id'] = '52ac2e99747aec013fcf4e6f'
    # kargs['year'] = 2019
    # kargs['wenli'] = 2
    # kargs['page_num'] = 3
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4063523 fadinKtTMMPz/uDnv27CnTgDMcoFK9i8+pZKlqlmf8IXYXnNuD7cBlB9G3oJIOXk'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Length': '221'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Origin': 'https://www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/web/school?type=2&sch_id=' + kargs['sch_id'] + ''
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    # batch控制一批还是二批，diploma_id控制本科还是专科
    payload = {"sch_id": "" + kargs['sch_id'] + "", "stu_province_id": "130000000000",
               "enroll_unit_id": "" + kargs['sch_id'] + "", "enroll_adm_type": 2}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.post(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    result = site_json['data']['drop_box']
    print('进度：:', kargs['page_num'])
    return result


def download_page_school_score(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4063523 fadinKtTMMPz/uDnv27CnTgDMcoFK9i8+pZKlqlmf8IXYXnNuD7cBlB9G3oJIOXk'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Length': '221'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Origin': 'https://www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/web/school?type=2&sch_id=' + kargs['sch_id'] + ''
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    payload = {"page": 1, "page_size": 10, "sch_id": kargs['sch_id'],
               "enroll_unit_id": kargs['sch_id'], "enroll_category": 1, "enroll_mode": 1,
               "diploma_id": 1,
               "stu_province_id": "130000000000", "wenli": kargs['wenli'], "only_admission": True}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.post(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    result = site_json['data']['eu_list']
    print('进度：:', kargs['page_num'])
    return result


def download_page_major_score(url, **kargs):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    newHeaders = {'Accept': 'application/json'
        , 'Accept-Encoding': 'gzip, deflate, br'
        , 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        , 'Authorization': '4063523 fadinKtTMMPz/uDnv27CnTgDMcoFK9i8+pZKlqlmf8IXYXnNuD7cBlB9G3oJIOXk'
        , 'Channel': 'www.wmzy.com pc'
        , 'Connection': 'keep-alive'
        , 'Content-Length': '221'
        , 'Content-Type': 'application/json'
        , 'Host': 'www.wmzy.com'
        , 'Origin': 'https://www.wmzy.com'
        , 'Referer': 'https://www.wmzy.com/web/school?type=2&sch_id=' + kargs['sch_id'] + ''
        , 'Sec-Fetch-Dest': 'empty'
        , 'Sec-Fetch-Mode': 'cors'
        , 'Sec-Fetch-Site': 'same-origin'
        ,
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        , 'x-requested-with': 'XMLHttpRequest'}
    cookie_jar = RequestsCookieJar()
    # batch控制一批还是二批，diploma_id控制本科还是专科
    payload = {"page_size": 100, "stu_province_id": "130000000000", "enroll_category": 1, "enroll_mode": 1,
               "enroll_unit_id": "" + kargs['sch_id'] + "", "sort_key": "min_score", "sort_type": 1,
               "only_admission": True, "page": 1, "year": kargs['academic_year'], "enroll_year": kargs['academic_year'],
               "wenli": kargs['wenli'],
               "academic_year": kargs['academic_year'],
               "diploma_id": kargs['diploma_id'], "batch": kargs['batch'], "batch_ex": kargs['batch_ex'],
               "enroll_stage": kargs['enroll_stage']}
    for c in cookies:
        cookie_jar.set(c['name'], c['value'], domain="wmzy.com")
    page = requests.post(url, cookies=cookie_jar, headers=newHeaders, json=payload)
    soup = BeautifulSoup(page.text, 'html.parser', from_encoding='utf-8')
    site_json = json.loads(soup.text)
    result = site_json['data']['enroll_info_list']
    print('进度：:', kargs['page_num'])
    return result


def spider_all_university():
    result = []
    for i in range(1, 140):
        result = result + download_page_university('https://www.wmzy.com/gw/api/sku/sku_service/sch_complete', i)
    pickle.dump(result, open(PATH_UNIVERSITY + 'university' + '.pkl', 'wb'))


def spider_all_school_score(inter):
    sp = SpiderData()
    list_university = sp.get_university_index()[inter[0]:inter[1]]
    result_f = []
    for i, one_data in enumerate(list_university):
        index = one_data['result']
        if index is None:
            result_f.append({'sch_id': one_data['sch_id']})
            continue
        for wenli_i in [1, 2]:
            args = {}
            args['sch_id'] = one_data['sch_id']
            args['wenli'] = wenli_i
            args['page_num'] = i
            result = download_page_school_score(
                'https://www.wmzy.com/gw/api/sku/enroll_admission_service/sch_enroll_data', **args)
            args['result'] = result
            result_f.append(args)
    return result_f


#
def spider_all_major_score(inter):
    sp = SpiderData()
    data = sp.get_university_index()
    list_university = data[inter[0]:inter[1]]
    result_f = []
    for i, one_data in enumerate(list_university):
        index = one_data['result']
        if index is None:
            result_f.append({'sch_id': one_data['sch_id']})
            continue
        for one_index in index:
            one_index['sch_id'] = one_data['sch_id']
            one_index['page_num'] = i
            result = download_page_major_score(
                'https://www.wmzy.com/gw/api/sku/enroll_admission_service/major_enroll_data', **one_index)
            one_index['result'] = result
            result_f.append(one_index)
    return result_f


def spider_all_university_index(inter):
    sp = SpiderData()
    list_university = sp.get_university()[inter[0]:inter[1]]
    result_f = []
    kargs = {}
    for i, one_data in enumerate(list_university):
        kargs['sch_id'] = one_data['sch_id']
        kargs['page_num'] = i
        result = download_page_index(
            'https://www.wmzy.com/gw/enroll_admission_service/sku_enroll_adm_data_drop_box', **kargs)
        result_f.append({'sch_id': kargs['sch_id'], 'result': result})
    return result_f


class SpiderData(object):

    def __init__(self):
        self.basic_path = '/Users/kunyue/project_personal/my_project/score_traitor/data/data_spider/data_university/'

    def __search_print(self, data, university=None):
        result = []
        for one_s in data:
            if one_s['sch_id'] == university:
                result.append(one_s)

        js = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ':'))
        print(js)
        return result

    def get_university_by_name(self, name):
        data = pickle.load(open(
            self.basic_path + 'university.pkl', "rb"))
        for one_s in data:
            if one_s['sch_name'] == name:
                return one_s['sch_id']

    def get_university(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'university.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    def get_university_index(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_university_index.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    def get_university_score(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_school_score.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    def get_university_major_score(self, university=None, university_name=None):
        data = pickle.load(open(
            self.basic_path + 'spider_all_major_score.pkl', "rb"))
        print('长度为：', len(data))
        if university is not None or university_name is not None:
            id = university if university is not None else self.get_university_by_name(university_name)
            return self.__search_print(data, id)
        return data

    def get_major_payload_by_university_name(self, university_name=None, year=2018, wenli=2):
        list_university = self.get_university_index(university_name=university_name)
        result_f = []
        for i, one_data in enumerate(list_university):
            index = one_data['result']
            if index is None:
                result_f.append({'sch_id': one_data['sch_id']})
                continue
            for one_index in index:
                one_index['sch_id'] = one_data['sch_id']
                one_index['page_num'] = i
                if one_index['academic_year'] == year and one_index['wenli'] == wenli:
                    result_f.append(one_index)
        return result_f


def mul_thread_run(func):
    pool = ThreadPool()
    args = []
    for i in range(8):
        args.append((int(2800 / 8 * i), int(2800 / 8 * (i + 1))))
    print(args)
    results = pool.map(func, args)
    pool.close()
    pool.join()
    result_final = []
    for one_result in results:
        result_final += one_result
    pickle.dump(result_final,
                open(PATH_UNIVERSITY + func.__name__ + '.pkl', 'wb'))


if __name__ == '__main__':
    sp = SpiderData()
    data = sp.get_university_major_score(university_name='河北工业大学')
    #
    # mul_thread_run(spider_all_major_score)
    # get_university_index()
    # get_university_major_score()
    # get_university()

    # 自定义专业爬虫
    # sp = SpiderData()
    # result = sp.get_major_payload_by_university_name('电子科技大学')[0]
    # result_tmp = download_page_major_score('https://www.wmzy.com/gw/api/sku/enroll_admission_service/major_enroll_data',**result)
    # print(result_tmp)
    # download_page_index('https://www.wmzy.com/gw/enroll_admission_service/sku_enroll_adm_data_drop_box')

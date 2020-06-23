from pyspider.libs.base_handler import *
import pandas as pd
import json


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.liqucn.com/rj/new/?page=1', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        # 获取最后一页的页码
        totle = int(response.doc(".current").text())
        for page in range(1, totle + 1):
            self.crawl('http://www.liqucn.com/rj/new/?page={}'.format(page), callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        docs = response.doc(".tip_blist li").items()
        dicts = []
        for item in docs:
            title = item(".tip_list>span>a").text()
            pubdate = item(".tip_list>i:eq(0)").text()
            info = item(".tip_list>i:eq(1)").text()
            # 手机类型
            category = info.split("：")[1]
            size = info.split("/")
            if len(size) == 2:
                size = size[1]
            else:
                size = "0MB"
            app_type = item("p").text()
            mobile_type = item("h3>a").text()
            # 保存数据

            # 建立图片下载渠道

            img_url = item(".tip_list>a>img").attr("src")
            # 获取文件名字
            filename = img_url[img_url.rindex("/") + 1:]
            # 添加软件logo图片下载地址
            self.crawl(img_url, callback=self.save_img, save={"filename": filename}, validate_cert=False)
            dicts.append({
                "title": title,
                "pubdate": pubdate,
                "category": category,
                "size": size,
                "app_type": app_type,
                "mobile_type": mobile_type

            })
        return dicts

    def on_result(self, result):
        if result:
            self.save_to_mongo(result)

    def save_to_mongo(self, result):
        df = pd.DataFrame(result)
        print(df)
        # content = json.loads(df.T.to_json()).values()


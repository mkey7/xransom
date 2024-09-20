"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
Codé par @JMousqueton pour Ransomware.live
"""

# from bs4 import BeautifulSoup
from lxml import etree


# 单独爬取一个post
def get_post(scrapy, site, url):
    try:
        page = scrapy.scrape(site, url)

        if page is None:
            return None

        # todo 提取相关字段
        html = etree.HTML(page["page_source"])
        post_title = html.xpath("//h3/text()")

        contents = ""
        bodys = html.xpath("//text()")
        for body in bodys:
            contents += body

        images = html.xpath("//div[@class='row']//img/@src")

        scrapy.appender(post_title, "meow", contents, "", post_url=url,
                        images=images, page=page)
    except Exception as e:
        print('meow: ' + 'parsing fail: ' + url + f"{e}")


def main(scrapy, page, site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])
        hrefs = html.xpath("//div[@class='card-body text-center']/a[1]/@href")
        for href in hrefs:
            post_url = "http://" + url + href
            get_post(scrapy, site, post_url)

    except Exception as e:
        print('meow: ' + 'parsing fail: ' + url + f"{e}")

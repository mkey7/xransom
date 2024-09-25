"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |         |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""

from bs4 import BeautifulSoup
from lxml import etree


# 单独爬取一个post
def get_post(scrapy, site, url):
    try:
        page = scrapy.scrape(site, url)

        if page is None:
            return None

        # todo 提取相关字段
        html = etree.HTML(page["page_source"])
        post_title = html.xpath("//h5/text()")

        contents = ""
        bodys = html.xpath("//text()")
        for body in bodys:
            contents += body

        published = html.xpath("//div[@class='css-1j63rwj']/p[last()]/text()")

        website = html.xpath("//div[@class='css-1j63rwj']//p[contains(@text,'website:')]/text()")
        website = website.splite(":")[-1]

        download = html.xpath("//div[@class='MuiBox-root css-4h4iek']//a[contains(@text,'http')]/@href")
        downloads = [download]

        scrapy.appender(post_title, "meow", contents, website, post_url=url,
                        published=published, download=downloads, page=page)
    except Exception as e:
        print('meow: ' + 'parsing fail: ' + url + f"{e}")


def main(scrapy, page, site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])
        hrefs = html.xpath("//div[@class='MuiBox-root css-16lsen3']/a/@href")
        for href in hrefs:
            post_url = url+href
            get_post(scrapy, site, post_url)

    except Exception as e:
        print(f'moneymessage: parsing fail: {url} : {e}')

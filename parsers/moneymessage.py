"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |         |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""

from lxml import etree


# 单独爬取一个post
def get_post(scrapy, site, url):
    try:
        page = scrapy.scrape(site, url)

        if page is None:
            return None

        # todo 提取相关字段
        html = etree.HTML(page["page_source"])
        post_title = html.xpath("//h5/text()")[0]

        contents = ""
        bodys = html.xpath("//text()")
        for body in bodys:
            contents += body

        published = html.xpath("//div[@class='MuiBox-root css-4h4iek'][last()]/p[1]/text()")[0]

        ps = html.xpath("//div[@class='css-1j63rwj']//p/text()")
        
        website = ""
        price = ""
        for p in ps:
            if p.lower().startswith("website"):
                website = p.split(" ")[-1]

            if p.lower().startswith("revenue"):
                price = p.split(" ")[-1]

        download = html.xpath("//div[@class='MuiBox-root css-4h4iek']//a[contains(@text,'http')]/@href")

        scrapy.appender(post_title, "moneymessage", contents, website,
                        post_url=url, published=published, download=download,
                        price =price, page=page)
    except Exception as e:
        print(f'moneymessage: parsing fail: {url} : {e}')


def main(scrapy, page, site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])
        hrefs = html.xpath("//div[@class='MuiBox-root css-16lsen3']/a/@href")
        for href in hrefs:
            post_url = "http://"+url+href
            get_post(scrapy, site, post_url)

    except Exception as e:
        print(f'moneymessage: parsing fail: {url} : {e}')

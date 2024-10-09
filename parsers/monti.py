
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url="")
"""

from lxml import etree


# 单独爬取一个post
def get_post(scrapy, site, url, published):
    try:
        page = scrapy.scrape(site, url)

        if page is None:
            return None

        # todo 提取相关字段
        html = etree.HTML(page["page_source"])
        post_title = html.xpath("//h2/text()")[0]

        contents = ""
        bodys = html.xpath("//text()")
        for body in bodys:
            contents += body

        download = html.xpath("//a[@target='_blank']/@href")

        scrapy.appender(post_title, "monti", contents, "", post_url=url,
                        published=published, download=download, page=page)
    except Exception as e:
        print(f'monti: parsing fail: {url} : {e}')


def main(scrapy, page, site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])
        hrefs = html.xpath("//a[@class='leak-card p-3']/@href")
        publisheds = html.xpath("//a[@class='leak-card p-3']//div[@class='col-auto published']")
        for href in range(0, len(hrefs)):
            post_url = "http://" + url + hrefs[href]
            published = publisheds[href]

            get_post(scrapy, site, post_url, published)

    except Exception as e:
        print(f'monti: parsing fail: {url} : {e}')

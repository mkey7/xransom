
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
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
        post_title = html.xpath("//h1/text()")[0]

        all_text = html.xpath("//text()")
        contents = " ".join(text.strip() for text in all_text if text.strip())

# 提取下载链接
        downloads = html.xpath("//div@[class='card-body']/p/text()")

        scrapy.appender(post_title, "ransomhub", contents, post_title,
                        post_url=url, published=published, download=downloads,
                        page=page)
    except Exception as e:
        print(f'ransomhub: parsing fail: {url} : {e}')


def main(scrapy, page, site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])
        post_urls = html.xpath("//div[@class='row']//a/@href")
        published = html.xpath("//div[@class='row']//div[@class='card-footer']/text()")
        for i in range(post_urls):
            post_url = url+'/'+post_urls[i]
            get_post(scrapy, site, post_url, published[i])

    except Exception as e:
        print(f'ransomhub: parsing fail: {url} : {e}')

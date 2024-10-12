"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |     X    |
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
        post_title = html.xpath("//h1/text()")[0]

        all_text = html.xpath("//text()")
        contents = " ".join(text.strip() for text in all_text if text.strip())

        published = html.xpath("//time/text()")[0]

# 提取下载链接
        downloads = html.xpath("//div[@class='entry-content']//a/@href")

        scrapy.appender(post_title, "ransomexx", contents, '', post_url=url,
                        published=published, download=downloads, page=page)
    except Exception as e:
        print(f'ransomexx: parsing fail: {url} : {e}')


def main(scrapy, page, site):
    url = page["domain"]
    try:

        html = etree.HTML(page["page_source"])
        post_urls = html.xpath("//h2/a/@href")

        for post_url in post_urls:
            post_url = "http://" + url + post_url
            get_post(scrapy, site, post_url)

    except Exception as e:
        print(f'ransomexx: parsing fail: {url} : {e}')




"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |      X         |                  |     x    |
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
        post_title = html.xpath("//div[@class='list-group-item rounded-3 py-3 bg-body-secondary text-bg-dark mb-2 position-relative']/text()")[0]

        all_text = html.xpath("//text()")
        contents = " ".join(text.strip() for text in all_text if text.strip())

        website = html.xpath("//div[@class='list-group-item rounded-3 py-3 bg-body-secondary text-bg-dark mb-2 position-relative']//p/a/@href")[0]

        published = html.xpath("//div[@class='d-flex gap-2 small mt-1 opacity-25']/div/2/b/text()")[0]

# 提取下载链接
        download = html.xpath("//div[@class='list-group-item rounded-3 py-3 bg-body-secondary text-bg-dark mb-2 position-relative']//p/a/@href")[1]
        downloads = [download]

        scrapy.appender(post_title, "8base", contents, website, post_url=url,
                        published=published, download=downloads, page=page)
    except Exception as e:
        print(f'8base: parsing fail: {url} : {e}')


def main(scrapy, page, site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])
        post_urls = html.xpath("//div[@div='list-group d-grid gap-2 border-0 mt-5']/a")
        for post_url in post_urls:

            get_post(scrapy, site, post_url)

    except Exception as e:
        print(f'8base: parsing fail: {url} : {e}')

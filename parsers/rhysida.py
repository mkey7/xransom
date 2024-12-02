
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
def get_post(scrapy, site, url):
    try:
        page = scrapy.scrape(site, url)

        if page is None:
            return None

        # todo 提取相关字段
        html = etree.HTML(page["page_source"])
        post_title = html.xpath("//div[@class='col-8']/p[@class='h4']/a/text()")[0]
        website = html.xpath("//div[@class='col-8']//a/@href")[0]

        all_text = html.xpath("//text()")
        contents = " ".join(text.strip() for text in all_text if text.strip())

        downloads = html.xpath(
            "//div[@class='col-8']//a[contains(text(), 'Documents')]/@href")

        scrapy.appender(post_title, "rhysida", contents, website, post_url=url,
                        download=downloads, page=page)
    except Exception as e:
        print(f'ERROR rhysida: parsing fail: {url} : {e}')


def main(scrapy, page, site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])
        post_urls = html.xpath("//div[@class='row m-2']//button/@data-company")

        for post_url in post_urls:
            post_url = url + '/archive.php?company=' + post_url
            get_post(scrapy, site, post_url)

    except Exception as e:
        print(f'ERROR rhysida: parsing fail: {url} : {e}')

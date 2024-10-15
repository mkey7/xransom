
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |      X         |                 |     x    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import re
from lxml import etree


# 单独爬取一个post
def get_post(scrapy, site, url):
    try:
        page = scrapy.scrape(site, url)

        if page is None:
            return None

        # todo 提取相关字段
        html = etree.HTML(page["page_source"])
        post_title = html.xpath("//h2/text()")[0]

        all_text = html.xpath("//text()")
        contents = " ".join(text.strip() for text in all_text if text.strip())

        published = html.xpath("//span[@id='timestampPost']/text()")[0]

        # 提取下载链接
        downloads = html.xpath("//div[@class='container-fluid full-browser']/a/@onclick")
        for i in range(len(downloads)):
            downloads[i] = downloads[i].split("'")[1]

        scrapy.appender(post_title, "threeam", contents, post_title, post_url=url,
                        published=published, download=downloads, page=page)
    except Exception as e:
        print(f'threeam: parsing fail: {url} : {e}')

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def main(scrapy, page, site):
    url = page["domain"]
    try:
        pattern = r'<a\s+href="(http://[^"]+)".*?>(.*?)</a>'
        matches = re.findall(pattern, page["page_source"])
        for match in matches:
            website = match[0]
            victim = remove_html_tags(match[1])
            #print(f"Website: {website}")
            #print(f"Victim: {victim}\n")                        
            scrapy.appender(victim, 'toufan', '',website,'','','IL',page=page)

    except:
        print('toufan: ' + 'parsing fail: '+url)

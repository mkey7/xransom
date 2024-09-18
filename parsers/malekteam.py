
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |     X    |
+------------------------------+------------------+----------+
"""

import os
from bs4 import BeautifulSoup
import re

# 单独爬取一个post
def get_post(scrapy,site,url):
    try:
        page = scrapy.scrape(site,url)

        if page == None:
            return None

        # todo 提取相关字段
        soup=BeautifulSoup(page["page_source"],'html.parser')
        post_title = soup.title.string
        post_title = post_title.replace("Malek Team:","")

        contents = ""
        head = soup.find("div",class_="section-timeline-heading")
        body = soup.find("div",class_="section-timeline")
        contents += head.get_text()
        contents += body.get_text()

        download = []
        downloads = body.find_all('li',class_="list-group-item")
        for li in downloads:
            download = site["domain"] + li.a["href"]
            download.appender(download)
        scrapy.appender(post_title, 'malekteam', contents,post_url=url,download=download,page=page)
    except:
        print('malekteam: ' + 'parsing fail: '+url)


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        for item in soup.find_all("div", class_="timeline_item"):
            # Extract 'Read More' link
            read_more_link = item.find("a", text="Read More")
            if read_more_link and read_more_link.has_attr('href'):
                post_url = read_more_link['href']
                post_url = site["domain"] + post_url 
                get_post(scrapy,site,post_url)
            #   scrapy.appender(date_text, 'malekteam', description,"","",post_url,page=page)

    except:
        print('malekteam: ' + 'parsing fail: '+url)

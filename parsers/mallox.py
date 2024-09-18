"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
"""

import os
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree

# 单独爬取一个post
def get_post(scrapy,site,url):
    try:
        page = scrapy.scrape(site,url)

        if page = None:
            return None
        html = etree.HTML(page["page_source"])

        post_title = html.xpath("//div[@class='text-gray-900 fs-2 fw-bold']/text()")

        content = html.xpath("//div[@class='fs-5 fw-semibold text-gray-600']/p/span/text()")
        contents = ""
        for c in content:
            contents += c

        scrapy.appender(post_title[0], 'malllox', contents,post_url=url,page=page)
    except:
        print('mallox: ' + 'parsing fail: '+url)

def main(scrapy,page,site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])

        hrefs = html.xpath("//div[@class='card']/div[2]/div[3]/a/@href")

        for href in hrefs:
            post_url = url + href

#        soup=BeautifulSoup(page["page_source"],'html.parser')
#        divs_name=soup.find_all('div', {"class": "card mb-4 box-shadow"})
#        for div in divs_name:
#            title = div.find('h4',{"class": "card-title"}).text.strip()
#            description = ''
#            for p in div.find_all('p'):
#                description+=p.text + ' '
#            post = div.find('a', {'class': 'btn btn-primary btn-sm'})
#            try: 
#                post = post.get('href')
#                post_url = url + post
#            except:
#                post_url = ''
#            publish = div.find('span', {'class': 'badge badge-info'}).text.strip()
#            date_obj = datetime.strptime(publish, "%d/%m/%Y %H:%M")
#            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
#            scrapy.appender(title, 'mallox', description,"",formatted_date,post_url,page=page)
#
    except:
        print('mallox: ' + 'parsing fail: '+url)

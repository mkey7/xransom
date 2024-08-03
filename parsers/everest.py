
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |         X      |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""

import os
from bs4 import BeautifulSoup


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('article')
        for div in divs_name:
            tmp = div.find('h2', {"class": "entry-title heading-size-1"})
            title = tmp.a.string
            a_tag = tmp.find('a')
            url = a_tag['href']
            description = div.find('div', {"class": "entry-content"}).p.text.strip()
            scrapy.appender(title, 'everest',description,'','',url,page=page)
    except:
        print('everest: ' + 'parsing fail: '+url)

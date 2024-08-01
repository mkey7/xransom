"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|              |               |        X         |    X     |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""

import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    blacklist=['HOME', 'HOW TO DOWNLOAD?', 'ARCHIVE']
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('span', {"class": "g-menu-item-title"})
        for div in divs_name:
            for item in div.contents :
                if item in blacklist:
                    continue
                post_url= url + str.lower(item.replace(".","-"))
                scrapy.appender(item, 'clop','_URL_','','',post_url)
    except:
        print('clop: ' + 'parsing fail: '+url)

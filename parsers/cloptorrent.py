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
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        tbody = soup.find('tbody')
        trs  = tbody.find_all('tr') # type: ignore
        for tr in trs:
            tds = tr.find_all('td')
            victim = tds[0].text.strip()
            #description = tds[2].text.strip()
            #appender(victim, 'clop','_URL_')
            download = tds[2].text.strip()
            scrapy.appender(victim,'clop',download=download)
    except:
        print('clop: ' + 'parsing fail: '+url)

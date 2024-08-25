"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |     X    |
+------------------------------+------------------+----------+
"""

import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        victim_links = soup.find_all('a', href=lambda href: href and not href.endswith("index.html"))
        for link in victim_links:
            if link['href'] != "#" and not link['href'].endswith("index.html"):
                post_url = url + link['href']
                victim = link.text.replace('[*] ','')
                scrapy.appender(victim, 'trisec', "","","",post_url,page=page)

    except:
        print('trisec: ' + 'parsing fail: '+url)
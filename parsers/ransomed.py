
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |    X     |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name  = soup.find_all('li',{"class":"wp-block-post"})
        for div in divs_name:
            meta = div.find('a')
            title = meta.text.strip()
            description = div.find('div',{"class":"wp-block-post-excerpt"}).text.strip()
            link = meta["href"]
            scrapy.appender(title, 'ransomed',description,'','',link,page=page)

    except:
        print('ransomed: ' + 'parsing fail: '+url)
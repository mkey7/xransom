
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('tr', {"class": "trow"})
        for div in divs_name:
            title = div.find_all('td')[0].text.strip()
            description = div.find_all('td')[2].text.strip()
            link = div.find('a')
            link = link.get('href')
            post_url = url + link
            scrapy.appender(title, 'rancoz', description,'','',post_url,page=page)

    except:
        print('rancoz: ' + 'parsing fail: '+url)
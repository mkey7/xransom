
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
from datetime import datetime


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name = soup.find_all('div',{"class":"publications-list__publication"})
        for div in divs_name:
            title = div.find("h3", class_="list-publication__name").text.strip()
            link = div.find("p", class_="list-publication__site").text.strip()
            description = div.find("p", class_="list-publication__description").text.strip()
            date = div.find("span", class_="publication-footer__date").text.strip()
            publication_date = datetime.strptime(date, "%d %B %Y").strftime("%Y-%m-%d %H:%M:%S.%f")
            scrapy.appender(title, 'dragonforce',description,link,publication_date,'')
    except:
        print('dragonforce: ' + 'parsing fail: '+url)


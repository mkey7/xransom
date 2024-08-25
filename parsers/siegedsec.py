"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |      X         |                 |     x    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os, re
from datetime import datetime
from bs4 import BeautifulSoup


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        rows = soup.find_all('tr')[1:]  # Exclude the first row (header)

        for row in rows:
            columns = row.find_all('td')
            victim = columns[0].get_text()
            description = columns[2].get_text()
            last_updated = columns[4].get_text()
            last_updated_datetime = datetime.strptime(last_updated, "%Y-%m-%d")
            published = last_updated_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
            link = url + "/" + columns[5].find('a')['href']
            scrapy.appender(victim, 'siegedsec', description.replace('\n',' '),"",published,link,page=page)

    except:
        print('siegedsec: ' + 'parsing fail: '+url)
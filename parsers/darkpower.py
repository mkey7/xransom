"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |          X       |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""

import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "sm:w-1/2 mb-10 px-4"})
        for div in divs_name:
            title = div.find('h2').text.strip()
            url = "powerj7kmpzkdhjg4szvcxxgktgk36ezpjxvtosylrpey7svpmrjyuyd"
            website = div.find('a')
            website = website.attrs['href']
            post_url = 'http://' + url + '.onion/' + website
            scrapy.appender(title,'darkpower','','', '', post_url)
    except:
        print('darkpower: ' + 'parsing fail: '+url)

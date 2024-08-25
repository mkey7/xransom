
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os,re
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        items = soup.find_all('div', class_='item')
        for item in items:
            victim = item.find('h3').text.strip()
            description = item.find('p').text.strip()
            link = item.find('a')['href']
            # button_link = item.find('a', href=True).get('href')
            button_link = item.find('a', href=lambda href: href and 'DataPage' in href)['href']
            post_url = url.replace('stm.html','') + button_link
    
            scrapy.appender(victim,'stormous',description,'','',post_url,page=page)

    except:
        print('stormous: ' + 'parsing fail: '+url)
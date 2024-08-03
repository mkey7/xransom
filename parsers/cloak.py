"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        main_items = soup.find_all('div', class_='main__items')
        for item in main_items:
            victim = item.find('h2').get_text()
            description = item.find('p', class_='main__country').get_text()
            link_element = item.find('a', class_='main__link')
            post_url = ''
            if link_element is not None:
                link = link_element['href'] 
                if link_element:
                    post_url =  post_url + link
            scrapy.appender(victim, 'cloak',description,'','',post_url,page=page)
    except:
        print('cloak: ' + 'parsing fail: '+url)
        pass


"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |     X    |
+------------------------------+------------------+----------+
"""

import os
from bs4 import BeautifulSoup
from datetime import datetime


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "list-group-item rounded-3 py-3 bg-body-secondary text-bg-dark mb-2 position-relative"})
        for div in divs_name:
            link = div.find(class_='stretched-link')
            victim = link.text.strip()  # Extract the link name as the victim
            post_url = link['href']      
            date_views_element = div.find(lambda tag: tag.name == 'div' and 'Downloaded:' in tag.text)
            date_views_text = date_views_element.text.strip()
             # Extract the Downloaded date
            downloaded_date = date_views_text.split("\n")[0].strip().replace('Downloaded:', '').strip()
            description = div.find('div', class_='small opacity-50').text.strip()
            
            formatted_date = datetime.strptime(downloaded_date, '%d.%m.%Y').strftime('%Y-%m-%d 00:00:00.000000')

            # def appender(post_title, group_name, description="", website="", published="", post_url=""):
            scrapy.appender(victim, 'cryptbb', description, '', formatted_date, post_url,page=page)
    except:
        print('cryptbb: ' + 'parsing fail: '+url)

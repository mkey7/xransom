
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |        X         |     X    |
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
        victim_elements = soup.find_all('div', class_='cart-block__content')

        for element in victim_elements: 
            victim_name_element = element.find_previous('h2', class_='cart-block__title', itemprop='name')
            victim_name = victim_name_element.text.strip()
            
            description = element.text.strip()
            
            published_time_element = element.find_next('time', itemprop='datePublished')
            published_time = published_time_element['datetime'] if published_time_element else None
            formatted_published_time = datetime.strptime(published_time, "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M:%S.%f")

            post_link_element = element.find_next('div', class_='cart-block__timer')
            if post_link_element:
                post_link = url + post_link_element['data-link'] 
            else: 
                post_link= ""
            

            scrapy.appender(victim_name,'werewolves',description,'',formatted_published_time,post_link,page=page)
    except:
        print('werewolves: ' + 'parsing fail: '+url)
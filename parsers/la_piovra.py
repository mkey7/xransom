
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
from datetime import datetime

# NOTE site中没有找到该组织的站点
def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs=soup.find_all('article')
        for article in divs:
            # Extract the title
            title = article.find('h2', class_='entry-title').text.strip()

            # Extract the URL
            url = article.find('h2', class_='entry-title').a['href']

            # Extract the datetime
            # Extract the datetime
            datetime_str = article.find('time', class_='entry-date')['datetime']
            datetime_obj = datetime.fromisoformat(datetime_str)
            published = datetime_obj.strftime('%Y-%m-%d %H:%M:%S.%f')

            description = article.find('div',{"class" : "entry-content"}).text.strip()

            scrapy.appender(title, 'la_piovra', description,"",published,url,page=page)
    except:
        print('la_piovra: ' + 'parsing fail: '+url)
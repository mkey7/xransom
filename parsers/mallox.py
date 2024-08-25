"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
"""

import os
from bs4 import BeautifulSoup
from datetime import datetime


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "card mb-4 box-shadow"})
        for div in divs_name:
            title = div.find('h4',{"class": "card-title"}).text.strip()
            description = ''
            for p in div.find_all('p'):
                description+=p.text + ' '
            post = div.find('a', {'class': 'btn btn-primary btn-sm'})
            try: 
                post = post.get('href')
                post_url = url + post
            except:
                post_url = ''
            publish = div.find('span', {'class': 'badge badge-info'}).text.strip()
            date_obj = datetime.strptime(publish, "%d/%m/%Y %H:%M")
            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
            scrapy.appender(title, 'mallox', description,"",formatted_date,post_url,page=page)

    except:
        print('mallox: ' + 'parsing fail: '+url)
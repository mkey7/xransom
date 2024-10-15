"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from bs4 import BeautifulSoup
from datetime import datetime


def main(scrapy, page, site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "ann-block"})
        for div in divs_name:
            title = div.find('div', {'class': 'a-b-n-name'}).text.strip()
            published = div.find('div', {'class': 'a-b-h-time'}).text.strip()
            date_obj = datetime.strptime(published, '%b %d, %Y %I:%M %p')
            published = datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S.%f')
            link = div.find('button', {'class': 'a-b-b-r-l-button'})
            link = link['onclick'].replace('window.location=','')
            link = url + link 
            description = div.find('div', {'class': 'a-b-text'}).text.strip()
            scrapy.appender(title, 'snatch', description,"",published,link.replace('\'',''),page=page)
    except:
        print('snatch: ' + 'parsing fail: '+url)

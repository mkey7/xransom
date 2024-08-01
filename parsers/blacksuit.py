
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
from sharedutils import errlog, find_slug_by_md5, extract_md5_from_filename

def main(scrapy,page,site):
    url_site = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs=soup.find_all('div', {"class": "card"})
        for article in divs:
            # Extract the title
            title = article.find('div', class_='title').text.strip()

            # Extract the URL
            url = article.find('div', class_='title').a['href']
            post_url = url_site + '/' +  url

            website= article.find('div', class_='url').a['href']
            try:
                description = article.find('p').text.strip().replace('\n', ' ')
            except:
                description = ''
            scrapy.appender(title, 'blacksuit', description,website,'',post_url)

    except:
        print('blacksuit: ' + 'parsing fail: '+url_site)
        pass

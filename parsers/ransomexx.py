"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "card-body"})
        for div in divs_name:
            title = div.find('h5').text.strip()
            description = div.find_all('p', {"class", "card-text"})[1].text.strip()
            link = div.find('a', {"class", "btn btn-outline-primary"})
            link = link.get('href')
            post_url = url + link
            scrapy.appender(title, 'ransomexx', description,"","",post_url,page=page)

    except:
        print('ransomexx: ' + 'parsing fail: '+url)
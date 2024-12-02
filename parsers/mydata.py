
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
        divs_name=soup.find_all('div', class_='b_block')
        for div in divs_name:
            header = div.find('a', class_="a_title")
            title = header.text.strip()
            post = header.get('href') or header['href'] 
            description = div.find('div', style='line-height:20px; padding-top:5px; margin-bottom:30px;').text.strip()
            try:
                post_url = url + str(post)
            except:
                post_url = 'http://mydatae2d63il5oaxxangwnid5loq2qmtsol2ozr6vtb7yfm5ypzo6id.onion' +  "/" + str(post)
            scrapy.appender(title, 'mydata', description,"","",url,page=page)

    except:
        print('mydata: ' + 'parsing fail: '+url)

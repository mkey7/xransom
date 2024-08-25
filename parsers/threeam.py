
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
        post_divs = soup.find_all('div', class_='post')
        for post_div in post_divs:
            post_title = post_div.find('div', class_='post-title-block').text.strip()
            victim  = post_title.split('\n')[0].strip()
            description = post_div.find('div', class_='post-text').text.strip()
            link = post_div.find('a', class_='post-more-link')
            if link:
                onclick_attr = link.get('onclick')
                post = url +  onclick_attr.split("'")[1]
            scrapy.appender(victim, 'threeam', description,victim,'',post,page=page)

    except:
        print('threeam: ' + 'parsing fail: '+url)
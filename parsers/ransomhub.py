
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
import re

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        posts = soup.find_all('div', class_='timeline-item')
        for post in posts:
            title_element = post.find('h5', class_='card-title').find('a')
            match = re.match(r"^(.*?)<([^>]*)>", title_element.text)
            title = match.group(1).strip()  # Group 1: String before '<'
            website = match.group(2).strip()  # Group 2: String between '<' and '>'
            post_url = url + title_element['href']

            # date_element = post.find('div', class_='countdown-date')
            # description = date_element.text

            scrapy.appender(title, 'ransomhub', '',website,'',post_url,page=page)


    except:
        print('ransomhub: ' + 'parsing fail: '+ url)
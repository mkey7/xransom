"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |       X        |        X         |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import re
from bs4 import BeautifulSoup
import json


def main(scrapy, page, site):
    url = page["domain"]
    try:
        soup = BeautifulSoup(page["page_source"], 'html.parser')
        jsonpart = soup.pre.contents
        data = json.loads(jsonpart[0])
        for element in data['data']:
            title = element['header']
            link = element['id']
            post_url = url + link
            website = element['url']
            try:
                date_string = element['actionDate']
            except:
                formated_date = ''
            description = re.sub(r'<[^>]*>', '', element['info'])
            scrapy.appender(title, 'ransomhouse', description, website, "",
                            post_url, page=page)
    except:
        print('ransomhouse: ' + 'parsing fail: '+url)

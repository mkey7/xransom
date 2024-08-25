"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |          X       |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
import json
import html
import re
import datetime

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        jsonpart = soup.pre.contents
        data = json.loads(jsonpart[0])
        for entry in data['data']:
            title = html.unescape(entry['title'])
            website = str(entry['url'])
            post_url =  url + entry['id'].strip() 
            description = html.unescape((re.sub(r'<[^>]*>', '',entry['text'])))
            date_str = entry['time']
            dt_object = datetime.datetime.strptime(date_str, "%Y-%B-%d").replace(hour=1, minute=2, second=3, microsecond=456789)
            published = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")
            scrapy.appender(title, 'royal', description.replace('\n',''),website,published,post_url,page=page)
    except:
        print('royal: ' + 'parsing fail: '+url)
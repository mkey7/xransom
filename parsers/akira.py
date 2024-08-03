"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
import json
import html
import datetime

def main(scrapy,page,site):
    post_url = "https://akiral2iz6a7qgd3ayp3l6yub7xx2uep76idk3u2kollpj5z3z636bad.onion"
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        jsonpart = soup.pre.contents
        data = json.loads(jsonpart[0])
        for entry in data:
            title = html.unescape(entry['title'])
            date_str = entry['date']
            description = entry['content']
            #dt_object = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(hour=1, minute=2, second=3, microsecond=456789)
            dt_object = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            # Get the current time
            current_time = datetime.datetime.now().time()
            # Combine the parsed date with the current time
            combined_datetime = datetime.datetime.combine(dt_object.date(), current_time)
            published = combined_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
            #published = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")
            scrapy.appender(title.replace('\n',''), 'akira', description.replace('\n',''),'',published,post_url,page=page)
    except:
        print('akira: ' + 'parsing fail')
        pass    

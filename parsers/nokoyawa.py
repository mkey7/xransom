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
from datetime import datetime
from urllib.parse import unquote


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        try:
            jsonpart = soup.pre.contents
            data = json.loads(jsonpart[0])
            for entry in data['payload']:
                title = html.unescape(entry['title'])
                title = decoded_url = unquote(title)
                website = str(entry['url'])
                website = decoded_url = unquote(website)
                #url = find_slug_by_md5('nokoyawa', extract_md5_from_filename(html_doc))
                post_url =  url + '/leak/' +  entry['_id'].strip() 
                description = html.unescape((re.sub(r'<[^>]*>', '',entry['description'])))
                date_str = entry['createdAt']
                dt_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                # datetime.datetime.strptime(date_str, "%Y-%B-%d").replace(hour=1, minute=2, second=3, microsecond=456789)
                #published = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")
                published = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")
                scrapy.appender(title, 'nokoyawa', description.replace('\n',''),website,published,post_url,page=page)
        except:
            print('nokoyawa: is not a json file - parsing fail')

    except:
        print('incransom: ' + 'parsing fail: '+url)
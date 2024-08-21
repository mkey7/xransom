"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|       X     |      X         |                  |    X     |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""

import os
from bs4 import BeautifulSoup
from parse import appender
from datetime import datetime
from sharedutils import stdlog, errlog
import json
import re

def strip_html_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def cut_content_before_link(content):
        match = re.search(r"Download link", content)
        if match:
            return content[match.start():]
        return content

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        # Find the script tag containing JSON data
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

        # Extract JSON content from the script tag
        json_content = script_tag.string

        # Parse the JSON data
        data = json.loads(json_content)

        # Access the required information
        posts_data = data['props']['pageProps']['posts']['data']

        # Print slug, title, content, and publishedAt for each post
        for post in posts_data:
            title = post['attributes']['title']
            victim = title.split('\\')[0]
            price = title.split('\\')[1]
            country = title.split('\\')[2]
            website = title.split('\\')[0].strip() if '\\' in title else title.strip()                  
            published_at = datetime.strptime(post['attributes']['publishedAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
            postdate = published_at.strftime("%Y-%m-%d %H:%M:%S.%f")
            #victim =  post['attributes']['slug']
            content = strip_html_tags(post['attributes']['content'])
            content = cut_content_before_link(content).replace('6wuivqgrv2g7brcwhjw5co3vligiqowpumzkcyebku7i2busrvlxnzid','***************')
            post_url = post['attributes']['slug']  # Replace 'link_field' with actual field name
            post_url = url + post_url

            download = content[content.rfind('Mirror')+8:]
            description = content[content.find("#1")+2:content.rfind('Download link #1')]

            scrapy.appender(victim,'cactus',description,website,postdate,post_url,'',download,country,price=price,page=page)
    except:
        print('cactus: ' + 'parsing fail: '+url)
        pass

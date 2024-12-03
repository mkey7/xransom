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

def is_json(data):
    try:
        json_object = json.loads(data)
        return True
    except ValueError:
        return False


def main(scrapy, page, site):
    url = page["domain"]
    try:
        if not is_json(page["page_source"]):
            data = json.loads(page["page_source"])
            for element in data['data']:
                title = element['header']
                link = element['id']
                post_url = url + "/r/" + link
                website = element['url']
                description = element['info']
                publish_time = element["actionDate"]
                price = element["revenue"]
                download = ["http://zv7u2tclxajbgae6ba4jkisnkfkts3lk7lxlypmuqktrk42qmo2c7hqd.onion/"]

                apage = scrapy.scrape(site, url)
                scrapy.appender(title, 'ransomhouse', description, website, publish_time,
                                post_url, download=download, price=price, page=apage)
    except:
        print('ransomhouse: ' + 'parsing fail: '+url)

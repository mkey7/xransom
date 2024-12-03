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
            print(element)
            if "display" in element:
                continue
            title = element['header']
            print(title)
            post_url = url + "/r/" + element['id']
            website = element['url']
            description = element['info']
            publish_time = element["actionDate"]
            price = element["revenue"]
            download = ["http://zv7u2tclxajbgae6ba4jkisnkfkts3lk7lxlypmuqktrk42qmo2c7hqd.onion/"]

            apage = scrapy.scrape(site, post_url)
            scrapy.appender(title, 'ransomhouse', description, website, publish_time,
                            post_url, download=download, price=price, page=apage)

    except:
        print('ransomhouse: ' + 'parsing fail: '+url)

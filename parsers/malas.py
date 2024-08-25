"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     x    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""

import os
from datetime import datetime
import re
from html import unescape

# TODO 这个网页存在问题，需要重构
def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        html = file.read()

        titles = re.findall(r'<title>(.*?)</title>', html, re.DOTALL)
        links = re.findall(r'<link>(.*?)</link>', html, re.DOTALL)
        descriptions = re.findall(r'<description>(.*?)</description>', html, re.DOTALL)
        publisheds = re.findall(r'<pubDate>(.*?)</pubDate>', html, re.DOTALL)

        for title,link, published, description in zip(titles, links,publisheds,descriptions):
                parsed_date = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
                formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                encoded_description = unescape(description)
                clean_description = re.sub(r"<.*?>", "", encoded_description)
                convert_description = clean_description.replace('&rsquo;','`')
                appender(title,'malas',convert_description.replace('\n',' '),'',formatted_date,link)

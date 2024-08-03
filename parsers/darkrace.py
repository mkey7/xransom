
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |      X         |                  |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
from datetime import datetime

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all("li", {"class": "post-list-item"})
        for div in divs_name:
            title = div.find("h2").text
            date_string = div.find("p", {"class": "post-info"}).text.strip()
            date_object = datetime.strptime(date_string, "%m/%d/%Y")
            published = date_object.strftime("%Y-%m-%d 00:00:00.00000")
            description = div.find("div").text
            link = div.find("a", {"class": "read-more"})["href"]
            post_url = url + link
            scrapy.appender(title, 'darkrace', description, '', published, post_url,page=page)
    except:
        print('darkrace: ' + 'parsing fail: '+url)



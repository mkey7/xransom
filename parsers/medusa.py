
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

# 网站有验证码
def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "card"})
        for div in divs_name:
            link = div.get('data-id')
            post_url = url + link
            title = div.find('h3', {"class":"card-title"}).text
            description = div.find("div", {"class": "card-body"}).text.strip()
            published = div.find("div", {"class": "date-updated"}).text.strip() + '.12345'
            scrapy.appender(title, 'medusa', description.replace('\n',' '),'',published,post_url,page=page)

    except:
        print('medusa: ' + 'parsing fail: '+url)

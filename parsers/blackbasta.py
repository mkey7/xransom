
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                | include in desc  |     x    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "card"})
        for div in divs_name:
            title = div.find('a', {"class": "blog_name_link"})
            post = title.get('href').replace("https","http").replace(" ","%20")
            title = title.text.strip()
            descs = div.find_all('p')
            description = ''
            website = ''
            print(post)
            for desc in descs:
                description += desc.text.strip()
                if 'SITE:' in desc.get_text():
                    website = desc.get_text()
                    website = website[website.find('w'):]
            scrapy.appender(title, 'blackbasta', description.replace('\n',' ').replace('ADDRESS',' Address '),website,'',post,page=page)
    except:
        print('blackbasta: ' + 'parsing fail')
        pass    

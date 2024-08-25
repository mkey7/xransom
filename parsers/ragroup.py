"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup

def remove_period_if_first_char(input_string):
    if input_string and input_string[0] == ".":
        return input_string[1:]
    else:
        return input_string

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "row"})
        for div in divs_name:
            for item in div.find_all('a') :
                title = item.text.strip()
                url = item['href']
                post_url = url + remove_period_if_first_char(url)
                title = title.replace('(Unpay-Full public)','')
                title = title.replace('(Unpay)','')
                title = title.replace('(Unpay-Partially public)','')
                title = title.replace('(Unpay-Start Leaking)','')
                title = title.replace('\t','')
                if len(title) > 0: 
                    scrapy.appender(title, 'ragroup', '','','',post_url,page=page)

    except:
        print('ragroup: ' + 'parsing fail: '+url)
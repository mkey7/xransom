"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |        X         |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup

# TODO 该这个网站了
# NOTE 网站没能打开
def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "card-body p-3 pt-2"})
        for div in divs_name:
            tmp = div.find('a',{"class":"h5"})
            title = tmp.text 
            print('Title : ' + title)
            post = tmp.get('href')
            url =  url + post
            description = div.find("p").text.strip()
            scrapy.appender(title, 'knight',description.replace('\n',' '),'','',url,page=page)
        divs_name=soup.find_all('div', {"class": "card-body"})
        for div in divs_name:
            try:
                h2 = div.find('h2',{"class":"card-title"})
                if h2:
                    title = h2.text.strip()
                    description = div.find("p").text.strip()
                    post = h2.a['href']
                    url =  url + post
                    scrapy.appender(title.replace('(leaking)',''), 'knight', description.replace('\n',''),'','',url,page=page)
            except:
                pass
    except:
        print('knight: ' + 'parsing fail: '+url)
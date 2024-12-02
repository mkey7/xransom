"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
Codé par @JMousqueton pour Ransomware.live
"""

from bs4 import BeautifulSoup
from datetime import datetime

# NOTE lockbit3组织改版了，需要验证登录，没法实现了
def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "post-block bad"})
        for div in divs_name:
            post = div['onclick'].split("'")[1]
            post_url = url + post
            title = div.find('div',{"class": "post-title"}).text.strip()
            description = div.find('div',{"class" : "post-block-text"}).text.strip()
            published = div.find('div',{"class" : "updated-post-date"}).text.strip()
            date_obj = datetime.strptime(published.replace('Updated: ',''), "%d %b, %Y,\xa0\xa0 %H:%M %Z")
            published = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
            scrapy.appender(title, 'lockbit3', description.replace('\n',''),"",published,post_url,page=page)
        divs_name=soup.find_all('div', {"class": "post-block good"})
        for div in divs_name:
            post = div['onclick'].split("'")[1]
            post_url = url + post
            title = div.find('div',{"class": "post-title"}).text.strip()
            description = div.find('div',{"class" : "post-block-text"}).text.strip()
            published = div.find('div',{"class" : "updated-post-date"}).text.strip()
            date_obj = datetime.strptime(published.replace('Updated: ',''), "%d %b, %Y,\xa0\xa0 %H:%M %Z")
            published = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
            scrapy.appender(title, 'lockbit3', description.replace('\n',''),"",published,post_url,page=page)
        divs_name=soup.find_all('a', {"class": "post-block bad"})
        for div in divs_name:
            title = div.find('div',{"class": "post-title"}).text.strip()
            description = div.find('div',{"class" : "post-block-text"}).text.strip()
            published = div.find('div',{"class" : "updated-post-date"}).text.strip()
            link = div['href']
            post_url = url + post
            published = div.find('div',{"class" : "updated-post-date"}).text.strip()
            date_obj = datetime.strptime(published.replace('Updated: ',''), "%d %b, %Y,\xa0\xa0 %H:%M %Z")
            published = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
            scrapy.appender(title, 'lockbit3', description.replace('\n',''),"",published,post_url,page=page)
        divs_name=soup.find_all('a', {"class": "post-block good"})
        for div in divs_name:
            title = div.find('div',{"class": "post-title"}).text.strip()
            description = div.find('div',{"class" : "post-block-text"}).text.strip()
            link = div['href']
            post_url = url + post
            published = div.find('div',{"class" : "updated-post-date"}).text.strip()
            date_obj = datetime.strptime(published.replace('Updated: ',''), "%d %b, %Y,\xa0\xa0 %H:%M %Z")
            published = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
            scrapy.appender(title, 'lockbit3', description.replace('\n',''),"",published,post_url,page=page)

    except:
        print('lockbit3: ' + 'parsing fail: '+url)


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
from datetime import datetime

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "d-flex flex-column justify-content-between flex-fill"})
        for div in divs_name:
            # <h2 data-v-8bca7b29="" class="fw-bold fs-5 mb-1"
            title = div.find('h2', {"title": "Company name"}).text.strip()
            # <div class="mb-2 text-justify" 
            description = div.find('small',{"class" : "text-justify"}).text.strip()
            # <div data-v-8bca7b29="" class="d-flex align-items-center mb-1"
            website = 'https://'+ div.find('div',{"title" : "Company site"}).text.strip()

            date_str = div.find('div',{"title" : "Created"}).text.strip()

            date_obj = datetime.strptime(date_str, '%d %b %Y')

            published = datetime.strftime(date_obj, '%Y-%m-%d %H:%M:%S.%f')

            #<a href="/post/9962b964-ac11-4bac-811d-d0bf10d81b24" class="btn btn-sm btn-primary h2 mb-0 fs-6"

            #post_url = 'http://' + url_site + '.onion/' +  url
            link_element = soup.find('a', class_="btn btn-sm btn-primary h2 mb-0")
            if link_element:
                link = link_element['href']
                post_url = url +  link
            else:
                post_url = ''
            scrapy.appender(title, 'noescape', description.replace('\n',' '),website,published,post_url,page=page)


    except:
        print('noescape: ' + 'parsing fail: '+url)
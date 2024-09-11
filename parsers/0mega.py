"""
+------------------------------+------------------+----------+------------+
| Description | Published Date | Victim's Website | Post URL | Downloads  |
+------------------------------+------------------+----------+------------+
|      X      |        X       |                  |     X    |      x     |
+------------------------------+------------------+----------+------------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
from datetime import datetime

def get_download(scrapy,url,site):
    page = scrapy.scrape(site,url)
    file = open(page["page_source"],'r')
    soup=BeautifulSoup(file,'html.parser')
    rows = soup.select('.tdownload') #[1:]
    downloads = []
    for row in rows:
    # for a in rows.select('a'):
        for a in row.find_all('a'):
            path = url[:url.rfind('onion')+5]+a['href']
            downloads.append(path)
    return downloads
    


def main(scrapy,page,site):
    try:
        file = open(page["page_source"],'r')
        soup=BeautifulSoup(file,'html.parser')
        rows = soup.select('.datatable tr.trow') #[1:]
        for row in rows:
            columns = row.find_all('td')
            title = columns[0].get_text(strip=True)
            last_updated_date_str = columns[4].get_text(strip=True)
            pubdate = datetime.strptime(last_updated_date_str, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S.%f")
            description = columns[2].get_text(strip=True)
            link = columns[5].find('a')['href']
            link = page["domain"] +str(link)
            print(link)
            downloads = get_download(scrapy,link,site)
            scrapy.appender(title, '0mega', description,"",pubdate,link,download=downloads,page=page)
    except:
        print('0mega: ' + 'parsing fail')
        pass

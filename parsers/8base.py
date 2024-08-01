
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |      X         |                  |     x    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from datetime import datetime
from bs4 import BeautifulSoup


def main(scrapy,page,site):
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', class_='list-group-item')
        for div in divs_name:
            link = div.find('a')['href']
            name = div.find('a').text.strip()
            tmp = div.find('div', class_='d-flex gap-2 small mt-1 opacity-25').text.strip()
            date_string = tmp.splitlines()[0].replace("Downloaded: ","")
            try: 
                published = datetime.strptime(date_string, "%d.%m.%Y").strftime("%Y-%m-%d %H:%M:%S.%f")
            except: 
                published = datetime.strptime(date_string, "%d.%m.%y").strftime("%Y-%m-%d %H:%M:%S.%f")
            description = div.find('div', class_='small opacity-50').text.strip()
            scrapy.appender(name, '8base', description.replace('\n',' '),"",published,link)
    except:
       print('8base : ' + 'parsing fail')
       pass    

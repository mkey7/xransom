
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        div_containers = soup.find_all('div', class_='border m-2 p-2')
        for div in div_containers:
            title_div = div.find('div', class_='m-2 h4')
            title = title_div.text.strip() if title_div else ''
            description_div = div.find('div', class_='m-2')
            description = description_div.text.strip().replace('\n',' ') if description_div else ''
            post_url=''
            try:
                post_url = url + '/archive.php?company=' + div.find('button')['data-company']
            except:
                pass
            if len(title) != 0: 
                scrapy.appender(title, 'rhysida', description,"","",post_url,page=page)

    except:
        print('rhysida: ' + 'parsing fail: '+url)
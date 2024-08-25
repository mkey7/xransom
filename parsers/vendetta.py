import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {'class':'post'})
        for div in divs_name:
            title = div.a['href'].split('/')[2]
            description = div.find('p', {'class': 'text'}).text.strip()
            scrapy.appender(title, 'vendetta', description,page=page)
    except:
        print('vendetta: ' + 'parsing fail: '+url)
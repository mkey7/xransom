import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {'class':'list-text'})
        for div in divs_name:
            title = div.a['href'].split('/')[2]
            if '.onion' not in title: 
                description = div.a.text.strip()
                scrapy.appender(title, 'cuba', description)
    except:
        print('cuda: ' + 'parsing fail: '+url)

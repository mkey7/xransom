import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "card"})
        for div in divs_name:
            title = div.find('h5', {"class": "card-brand"}).text.strip()
            description = div.find('div', {"class": "card-desc"}).text.strip()
            scrapy.appender(title, 'avoslocker',description.replace('\n',' '))
    except:
        print('avoslocker: ' + 'parsing fail')
        pass

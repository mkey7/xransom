import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "item_box"})
        for div in divs_name:
            title = div.find('a',{"class": "item_box-title mb-2 mt-1"}).text.strip()
            description = div.find('div',{"class": "item_box_text"}).text.strip()
            website = div.find('a',{"class": "item_box-info__link"}).text.strip()
            scrapy.appender(title, 'qilin', description.replace('\n',' '), website,page=page)

    except:
        print('qilin: ' + 'parsing fail: '+url)
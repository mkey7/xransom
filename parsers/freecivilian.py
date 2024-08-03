import os
from bs4 import BeautifulSoup
from parse import appender

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('section', {"id": "openSource"})
        for div in divs_name:
            for item in div.find_all('a',{'class':"a_href"}) :
                # (item.text.replace(' - ','#').split('#')[0].replace('+','').strip())
                scrapy.appender(item.text.replace(' - ','#').split('#')[0].replace('+','').strip(),'freecivilian',page=page)
    except:
        print('freecivilian: ' + 'parsing fail: '+url)

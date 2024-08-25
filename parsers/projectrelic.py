import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "content"})
        for div in divs_name:
            title = div.find('div', {'class': 'name'}).text.strip()
            description =  div.find('div', {'class': 'description'}).text.strip()
            # stdlog(title)
            scrapy.appender(title, 'projectrelic', description,page=page)

    except:
        print('projectrelic: ' + 'parsing fail: '+url)
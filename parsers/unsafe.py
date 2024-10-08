import os
import re
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "info"})
        for div in divs_name:
            title = str(div.find('h4').get_text())
            titre_h6 = div.find_all("h6")
            website = ''
            country = ''
            revenue = ''
            for info in titre_h6:
                if "website" in str(info.text):
                    website = re.sub(r'[^a-zA-Z0-9\.:/]', '', str(info.text.replace('website: ','https://')))
                if "country" in str(info.text): 
                    country = str(info.text)
                if "revenue" in str(info.text): 
                    revenue = str(info.text)
            description = country + ' -' + revenue
            scrapy.appender(title, 'unsafe', description, website,page=page)
    except:
        print('threeam: ' + 'parsing fail: '+url)
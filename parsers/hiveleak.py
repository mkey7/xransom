import re
from bs4 import BeautifulSoup
import json

def main(scrapy,page,site):
    url = page["domain"]
    try:
        htmlfile = page["page_source"]
        jsonfile = re.sub(r'<[^>]+>', '', htmlfile)
        data = json.loads(jsonfile)
        for element in data:
            title = element['title']
            website = element['website']
            try:
                description = element['description'].replace('\n',' ')
            except:
                pass
            scrapy.appender(title, 'hiveleak', description, website,page=page)
    except:
        print('hiveleak: ' + 'parsing fail: '+url)
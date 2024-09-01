
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                | include in desc  |     x    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup

# NOTE 打不开
def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        
        # Find all div elements with class "card" (assuming there may be more companies)
        companies = soup.find_all('div', class_='card')

        # Iterate through each company
        for company in companies:
            try: 
                victim = company.find('div', class_='card-header').text.strip()
            except: 
                continue
            description = company.find('div', class_='card-body').p.text.strip()
            website = company.find('a', href=True, text='Visit site')['href']
            scrapy.appender(victim, 'losttrust', description.replace('\n',' '),"https://"+website,page=page)

    except:
        print('losttrust: ' + 'parsing fail: '+url)
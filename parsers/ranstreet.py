
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |        X         |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        all_tr_elements = soup.find_all('tr')
        for tr in all_tr_elements:
            th_element = tr.find('th')  # Find the first <th> within each <tr>
            if th_element:
                company_name = th_element.text.strip().replace('C0MPANY [', '').replace(']', '')
                scrapy.appender(company_name,'ranstreet',page=page)

    except:
        print('ranstreet: ' + 'parsing fail: '+url)
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |        X         |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url="")
"""

import os
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('td',{"valign":"top"})
        for div in divs_name:
            try:
                title = div.find("font", {"size":4}).text.strip() 
                for description in div.find_all("font", {"size":2, "color":"#5B61F6"}):
                    if description.b.text.strip().startswith("http"):
                        website = description.get_text()
                    if not description.b.text.strip().startswith("http"):
                        desc = description.get_text()
                        scrapy.appender(title, 'vicesociety', desc,website,page=page)
            except:
                pass
    except:
        print('vicesociety: ' + 'parsing fail: '+url)
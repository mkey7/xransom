
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |          X       |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from bs4 import BeautifulSoup
import datetime

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('th', {"class": "News"})
        for div in divs_name:
            title = div.next_element.strip()
            description = div.find('i', {'class': 'location'}).next_sibling.strip()
            website = div.find('i', {'class': 'link'}).next_sibling.strip()
            post_url = url + '/topic.php?id='+div['onclick'].split("'")[1] 
            added_date = None
            div_text = div.find_next('div', {'style': 'line-height: 1.70;'}).get_text()
            if 'added:' in div_text:
                added_date = div_text.split('added:')[1].split('publication date:')[0].strip()
                now = datetime.datetime.now()
                added_date = f"{added_date} {now.strftime('%H:%M:%S.%f')}"
            scrapy.appender(title, 'play', description, website,added_date,post_url,page=page)

    except:
        print('play: ' + 'parsing fail: '+url)
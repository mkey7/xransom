"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "blog-posts"})
        for div in divs_name:
            title = div.find('h2').text.strip()
            descriptions = div.find_all('p')
            description=''
            for p in descriptions:
                description +=p.text.strip()
            scrapy.appender(title, 'crosslock', description,page=page)
    except:
        print('crosslock: ' + 'parsing fail: '+url)


"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('table', {"class": "table table-bordered table-content"})
        # <table class="table table-bordered table-content ">
        for div in divs_name:
            title = div.find('h1').text.strip()
            description = div.find('p').text.strip().replace("\n", "")
            website = div.find('a')
            website = website.attrs['href']
            scrapy.appender(title, 'blackbyte', description,website,page=page)
    except:
        print('blackbyte: ' + 'parsing fail')
        pass

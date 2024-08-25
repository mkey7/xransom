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
        #divs_name=soup.find_all('a', class_=["_m _preview grid__item", "_l _leaked grid__item"])
        div = soup.find('div', {"class": "grid"})
        divs_name = div.find_all('a') 
        for div in divs_name:
            #title = div.find('div', class_='grid-caption__title')
            title = div.find('div', {"class": "grid-caption__title"}).contents[0].strip() 
            #victim = title.text.strip().replace('\n','')
            #victim = re.split(r'  ',victim)[0]
            post = div.get('href')
            post_url = url + post
            scrapy.appender(title, 'trigona', '','','',post_url,page=page)

    except:
        print('trigona: ' + 'parsing fail: '+url)

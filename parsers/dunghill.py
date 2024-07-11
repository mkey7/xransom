"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
from sharedutils import errlog, get_website, stdlog
from parse import appender, existingpost

# TODO 爬取更详细的网页 还么有完成
def get_url(url):
    try:
        page = get_website(url,'dunghill_leak')
        soup=BeautifulSoup(page,'html.parser')
        head_tag = soup.find('div',class_='block-heading text-left')
        title = head_tag.get_text().strip()
        print('title:'+title+'!')
        
        
        div_tag = soup.find_next('div')
        print(div_tag)

        li_tag = soup.find_all('li')
        download = []
        for li in li_tag:
            hrefs = li.find_all('a')
            for h in hrefs:
                download.append(h['href'])
        print(download)


    except:
        errlog("failed to get : "+ url)


def main():
    group_name = 'dunghill_leak'
    for filename in os.listdir('source'):
        try:
            if filename.startswith('dunghill_leak-'):
                html_doc='source/'+filename
                file=open(html_doc,'r')
                soup=BeautifulSoup(file,'html.parser')
                divs = soup.find_all('div',class_="news-container")
                if not divs:
                    continue
                stdlog('find dunghill_leak index.html')
                divs = soup.find_all('div',{"class": "custom-container2"})
                for div in divs:
                    title = div.find('div', {"class": "ibody_title"}).text.strip()
                    if existingpost(title,group_name):
                        print(group_name + ' - ' + title +' is existed!')
                        continue
                    description = div.find("div", {"class": "ibody_body"}).find_all('p')
                    description = description[2].text.strip()
                    link = "http://p66slxmtum2ox4jpayco6ai3qfehd5urgrs4oximjzklxcol264driqd.onion/" + div.find('div', {"class": "ibody_ft_right"}).a['href']
                    print(link)
                    get_url(link)
                    # appender(title, 'dunghill', description,'','',link)
                divs = soup.find_all('div',{"class": "custom-container"})
                for div in divs:
                    title = div.find('div', {"class": "ibody_title"}).text.strip()
                    
                    if existingpost(title,group_name):
                        print(group_name + ' - ' + title +' is existed!')
                        continue

                    description = div.find("div", {"class": "ibody_body"}).find_all('p')
                    description = description[2].text.strip()
                    link = "http://p66slxmtum2ox4jpayco6ai3qfehd5urgrs4oximjzklxcol264driqd.onion/" + div.find('div', {"class": "ibody_ft_right"}).a['href']
                    print(link)

                    # get_url(link)
                    
                    # appender(title, 'dunghill', description,'','',link)
                file.close()
        except:
            errlog('dunghill_leak: ' + 'parsing fail')
            pass    

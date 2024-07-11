"""
+------------------------------+------------------+----------+------------+
| Description | Published Date | Victim's Website | Post URL | Downloads  |
+------------------------------+------------------+----------+------------+
|      X      |        X       |                  |     X    |      x     |
+------------------------------+------------------+----------+------------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
from sharedutils import errlog, find_slug_by_md5, extract_md5_from_filename, get_website,stdlog
from parse import appender
from datetime import datetime

def get_download(url):
    stdlog("0mega: find download => "+ url)
    context = get_website(url,'0mega')
    soup=BeautifulSoup(context,'html.parser')
    rows = soup.select('.tdownload') #[1:]
    stdlog("rows : "+str(rows))
    downloads = []
    for row in rows:
    # for a in rows.select('a'):
        print("row!!!")
        for a in row.find_all('a'):
            print(a['href'])
            path = url[:url.rfind('onion')+5]+a['href']
            print(path)
            downloads.append(path)
            stdlog("path : "+ path)
    return downloads
    


def main():
    for filename in os.listdir('source'):
        try:
            if filename.startswith('0mega-'):
                html_doc='source/'+filename
                file=open(html_doc,'r')
                soup=BeautifulSoup(file,'html.parser')
                rows = soup.select('.datatable tr.trow') #[1:]
                for row in rows:
                    columns = row.find_all('td')
                    title = columns[0].get_text(strip=True)
                    last_updated_date_str = columns[4].get_text(strip=True)
                    pubdate = datetime.strptime(last_updated_date_str, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S.%f")
                    description = columns[2].get_text(strip=True)
                    link = columns[5].find('a')['href']
                    link = find_slug_by_md5('0mega', extract_md5_from_filename(html_doc)) +str(link)
                    downloads = get_download(link)
                    appender(title, '0mega', description,"",pubdate,link,download=downloads)
                file.close()
        except:
            errlog('0mega: ' + 'parsing fail')
            pass

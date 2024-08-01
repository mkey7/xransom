
"""
+------------------------------+------------------+----------+----------+
| Description | Published Date | Victim's Website | Post URL | Downloads|
+------------------------------+------------------+----------+----------+
|      X      |                |        X         |     X    |     X    |
+------------------------------+------------------+----------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
import re


def main(scrapy,page,site):
    try:
        soup=BeautifulSoup(page['page_source'],'html.parser')
        predata=soup.find('pre')
        predata = predata.text
        index1 = predata.find('[')
        index2 = predata.rfind(']')
        predata = predata[index1:index2+1]
        # print(predata)
        # # 去除文本中的多余空格和换行符
        predata = predata.strip()
        # print(predata)

        # # 去除文本中的特殊字符 '&lt;' 和 '&gt;'
        predata = predata.replace('&lt;', '<').replace('&gt;', '>').replace('<br>','')
        # print(predata)
        
        datas = predata.split('},\n{')
        for data in datas:
            ptitle = r"'title' : '(.*)',"
            title = re.search(ptitle,data).group(1)
            description = data[data.find('full')+8:data.find("links")-30].replace('\'','').replace('+','').replace('/t            ','')
            pdownload = re.findall(r"http(.*)",data)
            downloads = []
            for i in pdownload:
                downloads.append("http"+i[:i.find('\"')])
            scrapy.appender(title, 'abyss', description,title,"","http://3ev4metjirohtdpshsqlkrqcmxq6zu3d7obrdhglpy5jpbr7whmlfgqd.onion/",download=downloads)

        # data = json.loads(predata)
        # print(data)
        # for div in divs_name:
            # title = div.find('h5',{"class": "card-title"}).text.strip()
            # description = div.find('p',{"class" : "card-text"}).text.strip()
            # appender(title, 'abyss', description.replace('\n',''))
    except:
        print('blackbasta: ' + 'parsing fail')
        pass    
    

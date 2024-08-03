"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |          |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from bs4 import BeautifulSoup

# TODO 爬取更详细的网页 还么有完成
def get_url(scrapy,site,url,title,published):
    try:
        page = scrapy.scrape(site,url)
        soup=BeautifulSoup(page["page_source"],'html.parser')
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
        print("failed to get : "+ url)


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs = soup.find_all('div',{"class": "custom-container2"})
        for div in divs:
            title = div.find('div', {"class": "ibody_title"}).text.strip()
            
            # 判断该勒索是否已被爬取
            p = {}
            p['ransom_name'] = page["platform"]
            p['title'] = title
            if scrapy.existingpost(p):
                print( page["platform"] + ' - ' + title +' is existed!')
                continue

            description = div.find("div", {"class": "ibody_body"}).find_all('p')
            description = description[2].text.strip()
            link = url + div.find('div', {"class": "ibody_ft_right"}).a['href']
            print(link)
            get_url(link)
            # appender(title, 'dunghill', description,'','',link)
        divs = soup.find_all('div',{"class": "custom-container"})
        for div in divs:
            title = div.find('div', {"class": "ibody_title"}).text.strip()
            
            # 判断该勒索是否已被爬取
            p = {}
            p['ransom_name'] = page["platform"]
            p['title'] = title
            if scrapy.existingpost(p):
                print( page["platform"] + ' - ' + title +' is existed!')
                continue

            description = div.find("div", {"class": "ibody_body"}).find_all('p')
            description = description[2].text.strip()
            link = url + div.find('div', {"class": "ibody_ft_right"}).a['href']
            print(link)

            # get_url(link)
            
            # appender(title, 'dunghill', description,'','',link)
    except:
        print('dunghill: ' + 'parsing fail: '+url)
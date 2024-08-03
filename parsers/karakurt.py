from bs4 import BeautifulSoup

def get_url(scrapy,site,post_url):
    try:
        page = scrapy.scrape(site,post_url)
        soup=BeautifulSoup(page["page_source"],'html.parser')
        title = soup.find("h1")
        post_date = soup.find("span",{"class":"post-date"})
        # 行业
        industry= soup.find("span",{"class":"post-category"})
        description = soup.find("article",{"class":"detail"}).p.get_text()

        scrapy.appender(title, 'karakurt', description,published=post_date,post_url=post_url,page=page)
    except:
        print('karakurt: ' + 'parsing fail: '+post_url)
        

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('article', {"class": "ciz-post"})
        for div in divs_name:
            title = div.h3.a.text.strip()
            link = url + div.find("h3").a['href']
            print(title+" : "+link)
            get_url(scrapy,site,link)
    except:
        print('karakurt: ' + 'parsing fail: '+url)

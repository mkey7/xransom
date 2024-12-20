
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |     X    |
+------------------------------+------------------+----------+
"""

from bs4 import BeautifulSoup

def get_description(scrapy,site,url,title,published):
    page = scrapy.scrape(site, url)

    print(url)
    # todo 提取相关字段
    soup = BeautifulSoup(page["page_source"], 'html.parser')
    post_title = soup.title.string

    body = soup.section
    if body.p.find('a'):
        website = body.p.a['href']
        description =  body.contents[1].string
    else:
        website = ''
        description =  body.contents[0].string
    email = 'deepmind@onionmail.org'
    
    target_paragraphs = body.find_all('p')

    for a in target_paragraphs:
        if "Revenue:" in a.get_text():
            price = a.get_text()
            price = price[price.find('$'):]
            
    download = []
    downloads = body.find_all('a')
    for b in downloads:
        if 'zip' in b['href']:
            download.append(b['href'])
    scrapy.appender(title, 'bianlian', description,website,published,url,email,download,page=page)

def main(scrapy,page,site):
    url = page["domain"]
    print(url)
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.select('li')
        for div in divs_name:
            post = url+div.a['href']
            print(post)
            title = div.a.string
            published = div.span.string
            
            try:
                #TODO 爬取具体网页
                get_description(scrapy,site,post,title,published)
            except:
                print('failed to get : '+post)
    except:
        print("Failed during : " + url)

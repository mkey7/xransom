"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |          X       |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from bs4 import BeautifulSoup
from lxml import etree


# 单独爬取一个post
def get_post(scrapy, site, url):
    try:
        page = scrapy.scrape(site, url)

        if page is None:
            return None

        # todo 提取相关字段
        html = etree.HTML(page["page_source"])
        post_title = html.xpath("//title/text()")[0]

        all_text = html.xpath("//text()")
        contents = " ".join(text.strip() for text in all_text if text.strip())

        title = html.xpath("//th[@class='News']/div[1]/text()")[0]
        country = html.xpath("//i[@class='location']/following-sibling::text()")[0].replace('\xa0', '')
        website = html.xpath("//i[@class='link']/following-sibling::text()")[0].replace('\xa0', '')

        published = html.xpath("//div[contains(text(), 'added:')]/text()")[0].replace("added: ", "")

# 提取下载链接
        downloads = html.xpath("//div[contains(text(), 'DOWNLOAD LINKS:')]/text()")
        for download_link in downloads:
            download_link.replace("\xa0DOWNLOAD LINKS: ", "")

        scrapy.appender(post_title, "play", contents, website, post_url=url,
                        published=published, download=downloads, country=country, page=page)
    except Exception as e:
        print(f'play: parsing fail: {url} : {e}')


def main(scrapy, page, site):
    url = page["domain"]
    try:
        html = etree.HTML(page["page_source"])
        args = html.xpath("//th[@class='News']/@onclick")
        for arg in args:
            post_url = 'http://' + url + '/topic.php?id=' + arg.split("'")[1]
            get_post(scrapy, site, post_url)

    except Exception as e:
        print(f'play: parsing fail: {url} : {e}')


#        soup=BeautifulSoup(page["page_source"],'html.parser')
#        divs_name=soup.find_all('th', {"class": "News"})
#        for div in divs_name:
#            title = div.next_element.strip()
#            description = div.find('i', {'class': 'location'}).next_sibling.strip()
#            website = div.find('i', {'class': 'link'}).next_sibling.strip()
#            post_url = url + '/topic.php?id='+div['onclick'].split("'")[1] 
#            added_date = None
#            div_text = div.find_next('div', {'style': 'line-height: 1.70;'}).get_text()
#            if 'added:' in div_text:
#                added_date = div_text.split('added:')[1].split('publication date:')[0].strip()
#                now = datetime.datetime.now()
#                added_date = f"{added_date} {now.strftime('%H:%M:%S.%f')}"
#            scrapy.appender(title, 'play', description, website,added_date,post_url,page=page)
#
#    except:
#        print('play: ' + 'parsing fail: '+url)

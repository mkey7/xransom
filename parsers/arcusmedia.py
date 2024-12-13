"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |     X    |
+------------------------------+------------------+----------+
"""

from bs4 import BeautifulSoup


def get_description(scrapy, site, url):
    page = scrapy.scrape(site, url)

    print(url)
    # todo 提取相关字段
    soup = BeautifulSoup(page["page_source"], 'html.parser')

    entry_title_div = soup.find('div', class_='entry-title mb-gutter last:mb-0')
    title = entry_title_div.find('h1').get_text(strip=True)

    content_div = soup.find('div', class_='kenta-article-content is-layout-constrained kenta-entry-content entry-content has-global-padding clearfix mx-auto')
    paragraphs = content_div.find_all('p')
    div_description = paragraphs[0]
    lines = div_description.get_text(separator='\n').split('\n')
    website = lines[0].strip()
    description = lines[0].strip()+" "+lines[1].strip()


    div_published = soup.find('span', class_='entry-date')
    published_time = div_published.find('time', class_='published')
    published = published_time['datetime']


    email = 'AlexanderPushkin@exploit.im'

    download = []
    mark_tags = soup.find_all('mark')
    for mark_tag in mark_tags:
        text = mark_tag.get_text(strip=True)
        http_index = text.find('http')
        # 如果找到了 'http'，返回包括 'http' 在内及其后的所有字符串
        if http_index != -1:
            text = text[http_index:]
            download.append(text)
    scrapy.appender(title, 'arcusmedia', description, website, published, url, email, download, page=page)


def main(scrapy, page, site):
    url = page["domain"]
    print(url)
    try:
        soup = BeautifulSoup(page["page_source"], 'html.parser')
        divs_name = soup.select('div.card-wrapper.w-full')
        for div in divs_name:
            link = div.find('a', class_='kenta-button kenta-button-right entry-read-more')
            post = link['href']
            print(post)

            try:
                # TODO 爬取具体网页
                get_description(scrapy, site, post)
            except:
                print('failed to get : ' + post)
    except:
        print("Failed during : " + url)

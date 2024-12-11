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

    div_title = soup.find('div', class_='offer__text')
    title = div_title.get_text(strip=True)
    website_no = title
    parts = website_no.split()
    website = parts[0]

    div_description = soup.find('div', class_='dsc__text', id='dsc__text')
    description = div_description.get_text(strip=True)

    div_published = soup.find('div', class_='deadline')
    deadline_text = div_published.get_text(strip=True)
    published = deadline_text.replace('Deadline: ', '').strip()


    email = 'bashe.team@onionmail.org'

    div_country = soup.find('div', class_='count__text')
    country = div_country.get_text(strip=True)

    download = []
    links = soup.find_all('a', target="_blank")
    hrefs = [link['href'] for link in links if 'href' in link.attrs]
    for href in hrefs:
        download.append(href)
    scrapy.appender(title, 'Apt73', description, website, published, url, email, download, country, page=page)


def main(scrapy, page, site):
    url = page["domain"]
    print(url)
    try:
        soup = BeautifulSoup(page["page_source"], 'html.parser')
        segment_box = soup.find('div', class_='segment__box')
        divs_name = segment_box.find_all('div', recursive=False)
        for div in divs_name:
            onclick = div.get('onclick')
            url_start = onclick.find("='")
            url_end = onclick.find("'", url_start + 2)
            url_path = onclick[url_start + 2:url_end]
            post = url + url_path
            print(post)

            try:
                # TODO 爬取具体网页
                get_description(scrapy, site, post)
            except:
                print('failed to get : ' + post)
    except:
        print("Failed during : " + url)

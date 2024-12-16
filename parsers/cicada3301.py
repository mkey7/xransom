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

    h2_tag = soup.find('h2', class_="font-bold text-yellow-500 mb-4 break-words uppercase", style="font-size: 17px;")
    title = h2_tag.get_text(strip=True)

    a_tag = soup.find('a', class_="text-blue-400 text-sm ml-1 hover:text-blue-300")
    website = a_tag['href']

    p_tag = soup.find('p', class_="mt-1 text-gray-400 text-mg mb-6 overflow-y-auto whitespace-pre-wrap rounded-lg")
    description = p_tag.get_text(strip=True)

    created_span = soup.find('span', class_="text-yellow-500 text-xs font-semibold uppercase tracking-widest", text="Created:")
    next_span = created_span.find_next_sibling('span')
    published = next_span.get_text(strip=True)


    email = ''

    download = []
    download_modal = soup.find('div', id="downloadModal")
    p_tag = download_modal.find('p', style="max-height: 600px;overflow-y: auto;", class_="mt-1 text-gray-400 text-mg mb-6 whitespace-pre-wrap rounded-lg")
    text_url = p_tag.get_text(strip=True)
    download.append(text_url)
    scrapy.appender(title, 'cicada3301', description, website, published, url, email, download, page=page)


def main(scrapy, page, site):
    url = page["domain"]
    print(url)
    try:
        soup = BeautifulSoup(page["page_source"], 'html.parser')
        divs = soup.find_all('div', class_='w-full sm:w-1/2 md:w-1/2 lg:w-1/3 xl:w-1/3 px-6 mb-12')
        for div in divs:
            a_tag = div.find('a', class_="inline-flex items-center justify-center bg-gray-800 text-white py-2 px-4 border border-gray-600 hover:border-gray-400 rounded shadow hover:shadow-md transform hover:scale-105 transition ease-in-out duration-300 text-sm font-medium absolute bottom-0 right-0 mb-3 mr-6")
            href_value = a_tag['href']
            post = url + href_value
            print(post)

            try:
                # TODO 爬取具体网页
                get_description(scrapy, site, post)
            except:
                print('failed to get : ' + post)
    except:
        print("Failed during : " + url)

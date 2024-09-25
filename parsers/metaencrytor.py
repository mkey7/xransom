"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |          X       |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
from bs4 import BeautifulSoup


def main(scrapy, page, site):
    url = page["domain"]
    try:
        soup = BeautifulSoup(page["page_source"], 'html.parser')
        cards = soup.find_all('div', class_='card-header')
        for card in cards:
            victim = card.get_text(strip=True)
            description = card.find_next('p', class_='card-text').get_text(strip=True)

            website_link = card.find_next('a', class_='btn btn-secondary btn-sm')
            website = website_link['href'] if website_link else None

            post_link = card.find_next('a', class_='btn btn-primary btn-sm')
            if post_link:
                post_url = url + post_link['href']
            else:
                post_url = None
            scrapy.appender(victim, 'metaencryptor', description,
                            website, '', post_url, page=page)

    except Exception as e:
        print(f'metaencryptor: parsing fail: {url} : {e}')

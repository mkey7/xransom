"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
Codé par @JMousqueton pour Ransomware.live
"""

import os
from bs4 import BeautifulSoup
from datetime import datetime

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        story_cards = soup.find_all('div', class_='MuiCard-root')
        for card in story_cards:
            # Extract information from each card
            card_link = card.find('a')['href']
            card_link = url + card_link
            title = card.find('div', class_='MuiTypography-h5').text.strip()
            
            # Convert date to desired format
            raw_date = card.find('p', class_='story-createdAt').text.strip()
            date_object = datetime.strptime(raw_date, '%d %B ,%Y')
            formatted_date = date_object.strftime('%Y-%m-%d %H:%M:%S.%f')


            #image_url = card.find('div', class_='MuiCardMedia-root')['style'].split('url("')[1].split('")')[0]
            leak_status = card.find('div', class_='MuiAlert-message').text.strip()

            scrapy.appender(title, "meow", leak_status, "", formatted_date, card_link,page=page)

    except:
        print('meow: ' + 'parsing fail: '+url)

"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os,re
from bs4 import BeautifulSoup
from datetime import datetime

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        # Find all the <div> elements with class "block-content"
        post_divs = soup.find_all('div', class_='block-content')

        # Iterate over each <div> element to extract the desired information
        for div in post_divs:
            # Extract the title
            title = div.find('h2').get_text(strip=True)

            # Extract the date string
            date_string = div.find('p', class_='fs-sm').find('span', class_='text-primary').next_sibling.strip()

            # Convert the date string to a datetime object
            date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

            # Format the date in the desired format
            formatted_date = date.strftime('%Y-%m-%d %H:%M:%S.%f')

            # Extract the description
            description = div.find("strong").text.strip().replace('\t', '').replace('\n', '')
            #descriptions = re.findall(r'<strong>(.*?)</strong>', str(div), re.DOTALL)
            #description = BeautifulSoup(descriptions[0], "html.parser").get_text().replace('\t', '').replace('\n', '')

            scrapy.appender(title, 'cyclops',description,'',formatted_date,page=page)
    except:
        print('cyclops: ' + 'parsing fail: '+url)

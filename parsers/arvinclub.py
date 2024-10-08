
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |        X         |     X    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import re
import datetime
from bs4 import BeautifulSoup

def main(scrapy,page,site):
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        post_desc_divs = soup.find_all('div', class_='row post-desc')
        for div in post_desc_divs:
            date_element = div.find('time', class_='post-date')
            date = date_element.get_text(strip=True) if date_element else "Date not found"
            # Add current year if date doesn't contain a year
            if not re.search(r'\d{4}', date):
                current_year = datetime.datetime.now().year
                date = f"{date} {current_year}"   
            # Separate digits from text in the date
            date = re.sub(r'(\d)([^\d])', r'\1 \2', date)
            date = date.replace('  ',' ')
            formatted_date = datetime.datetime.strptime(date, '%d %B %Y')
            date = formatted_date.replace(hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, second=datetime.datetime.now().second, microsecond=datetime.datetime.now().microsecond)
            highlight_divs = div.find_all_next('div', class_='highlight', limit=2)
            if len(highlight_divs) >= 2:
                post = highlight_divs[0].get_text(strip=True)
                website = highlight_divs[1].get_text(strip=True)
                scrapy.appender(post, 'arvinclub', '', website, str(date),page=page)
    except:
        print('arvinclub: ' + 'parsing fail')
        pass    

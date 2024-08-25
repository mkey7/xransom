
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |     X    |
+------------------------------+------------------+----------+
"""

from bs4 import BeautifulSoup
from datetime import datetime


# Define a function to convert the date format
def convert_date_format(date):
    # Split the input date string to extract the month, day, and year
    dates = date.split(', ')
    date_string = dates[1]+', '+dates[2]
    
    date_format = "%b %d, %Y"

    date_object = datetime.strptime(date_string, date_format)

    return date_object

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        row = soup.find('div', class_="row")
        post_elements = row.find_all("div",class_="post")
        for element in post_elements:
            h2_element = element.find("h2")
            website = h2_element.find('a')['href'] if h2_element.find('a') else ''
            title = h2_element.get_text()
            description = element.find('div').get_text()
            h5 = element.find_all('h5')
            date = h5[0].get_text()
            try:
                published = convert_date_format(date)
            except:
                published = ''
            
            down = url + h5[1].find('a')['id']

            scrapy.appender(title, 'ciphbit', description,website,published,url,download=down,page=page)
    except:
        print('ciphbit: ' + 'parsing fail: '+url)

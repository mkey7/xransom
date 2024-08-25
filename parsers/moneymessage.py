"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |        X       |                  |         |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""

import os
from bs4 import BeautifulSoup
from datetime import datetime

def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')

        # Find all <a> elements with the specified class
        a_elements = soup.find_all("a", class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-j1mjqc")

        # Extract the link, title, and date information and store them in lists
        links = [a["href"] for a in a_elements]
        titles = [a.find("p").get_text() for a in a_elements]

        # Print the extracted information
        for link, title in zip(links, titles):
            link = url + link
            linn = ""
            scrapy.appender(title, 'moneymessage', '','','',link,page=page)

        a_elements = soup.find_all("a", class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone css-xvpw3o")

        # Extract the link, title, and date information and store them in lists
        links = [a["href"] for a in a_elements]
        titles = [a.find("p").get_text() for a in a_elements]

        # Print the extracted information
        for link, title in zip(links, titles):
            link = url + link
            link = ""
            scrapy.appender(title, 'moneymessage', '','','',link,page=page)

    except:
        print('moneymessage: ' + 'parsing fail: '+url)



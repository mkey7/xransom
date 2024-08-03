"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |      X         |                  |    X     |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import os
from bs4 import BeautifulSoup
from parse import appender
from datetime import datetime
from sharedutils import errlog, find_slug_by_md5, extract_md5_from_filename,stdlog, proxies,get_website
from urllib.parse import urlparse
import requests

# TODO 从该网站的json
def getfromjson(url):
    try:
        response = requests.get(url, proxies=proxies,verify=False)
        response.raise_for_status()  # Check for any HTTP errors
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

    # Assuming the response contains JSON data, parse it
    json_data = response.json()
    return json_data

def main(scrapy,page,site):
    url = page["domain"]
    try:
        group_name = "incransom"
        url = "http://incbackrlasjesgpfu5brktfjknbqoahe2hhmqfhasc5fb56mtukn4yd.onion/api/blog/get-leaks"
        onion_url = "http://incblog7vmuq7rktic73r4ha4j757m3ptym37tyvifzp2roedyyzzxid.onion/blog/leak/"
        data = getfromjson(url)
        
        if data == None:
            print("incransom failed!")
            return 0

        print(data['payload'])

        for item in data['payload']:
            title = item['title']
            website = item['url']
            id = item['id']
            post_url = onion_url+id
            print("title:"+title)
            print("website:"+website)
            print("post_url:"+post_url)
            description = ''
            downloads = []
            
            try:
                web = get_website(post_url,group_name)
                apage = scrapy.scrape(site,post_url)
                soup=BeautifulSoup(apage["page_source"],'html.parser')

                description_tags=soup.find_all('div',class_="flex flex-col w-full")
                description = description_tags[1].get_text().strip()
                print('description'+description)

                download_tags = soup.find('div',class_="grid 2xl:grid-cols-3 xl:grid-cols-2 gap-5")
                if download_tags != None:
                    a_tags = download_tags.find_all('a')
                    for i in a_tags:
                        print(i['href'])
                        downloads.append(i['href'])
            except:
                print("incransom failed!")

            scrapy.appender(title,group_name,description,website,"",post_url,download=downloads,page=page)
    except:
        print('incransom: ' + 'parsing fail: '+url)
        
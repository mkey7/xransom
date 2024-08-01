import os
from bs4 import BeautifulSoup
import re


def main(scrapy,page,site):
    url = page["domain"]
    try:
        soup=BeautifulSoup(page["page_source"],'html.parser')
        divs_name=soup.find_all('div', {"class": "border border-warning card-body shadow-lg"})
        pattern = r"\((.*?)\)"  # 正则表达式模式
        for div in divs_name:
            title = div.find('h4').text.strip()
            website = div.find('h6').text.strip().replace("Web Site:", "")
            description = div.find('p').text.strip()
            download = ""

            match = re.search(pattern, title)

            matched_text = ""
            if match:
                matched_text = match.group(1)  # 使用group(1)获取第一个括号内匹配的内容
            else:
                print("没有找到匹配项")
            a_tags = div.find_all('a')
            for i in a_tags:
                if  "FULL LEAK" in i.text:
                    download = i.get('href')
            
            scrapy.appender(title, 'daixin', description, website,download=download,country=matched_text)
    except:
        print('daixin: ' + 'parsing fail: '+url)

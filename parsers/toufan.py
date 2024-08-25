
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |      X         |                 |     x    |
+------------------------------+------------------+----------+
Rappel : def appender(post_title, group_name, description="", website="", published="", post_url=""):
"""
import re

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def main(scrapy,page,site):
    url = page["domain"]
    try:
        pattern = r'<a\s+href="(http://[^"]+)".*?>(.*?)</a>'
        matches = re.findall(pattern, page["page_source"])
        for match in matches:
            website = match[0]
            victim = remove_html_tags(match[1])
            #print(f"Website: {website}")
            #print(f"Victim: {victim}\n")                        
            scrapy.appender(victim, 'toufan', '',website,'','','IL',page=page)

    except:
        print('toufan: ' + 'parsing fail: '+url)
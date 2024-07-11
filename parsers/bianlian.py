
"""
+------------------------------+------------------+----------+
| Description | Published Date | Victim's Website | Post URL |
+------------------------------+------------------+----------+
|      X      |                |                  |     X    |
+------------------------------+------------------+----------+
"""

import os, hashlib
from bs4 import BeautifulSoup
from sharedutils import stdlog,errlog,get_website
from parse import appender,existingpost

def get_description(post,title,published):

    hash_object = hashlib.md5()
    hash_object.update(post.encode('utf-8'))
    hex_digest = hash_object.hexdigest()
    filename = 'bianlian-' + hex_digest + '.html'
    
    if os.path.exists(filename):
        return True 

    name = os.path.join(os.getcwd(), 'source', filename)
    page = get_website(post,'bianlian')
    stdlog("fetching bianlian-"+title)
    
    # todo 提取相关字段
    soup=BeautifulSoup(page,'html.parser')
    post_title = soup.title.string

    body = soup.section
    if body.p.find('a'):
        website = body.p.a['href']
        description =  body.contents[1].string
    else:
        website = ''
        description =  body.contents[0].string
    screenshot_path = 'docs/screenshots/posts/' + hex_digest + '.png'
    email = 'deepmind@onionmail.org'
    
    target_paragraphs = body.find_all('p')

    for a in target_paragraphs:
        if "Revenue:" in a.get_text():
            price = a.get_text()
            price = price[price.find('$'):]
            
    download = []
    downloads = body.find_all('a')
    for b in downloads:
        if 'zip' in b['href']:
            download.append(b['href'])
    appender(title, 'bianlian', description,website,published,post,email,price,'',download)




def main():
    url = "http://bianlivemqbawcco4cx4a672k2fip3guyxudzurfqvdszafam3ofqgqd.onion"
    for filename in os.listdir('source'):
        try:
            if filename.startswith('bianlian-'):
                html_doc='source/'+filename
                file=open(html_doc,'r')
                soup=BeautifulSoup(file,'html.parser')
                if soup.title.string != "Companies - BianLian":
                    continue
                divs_name=soup.select('li')
                for div in divs_name:
                    post = url+div.a['href']
                    title = div.a.string
                    published = div.span.string
                    
                    try:
                        if existingpost(title,'bianlian'):
                            get_description(post,title,published)
                    except:
                        errlog('failed to get : '+post)
                file.close()
        except:
            errlog("Failed during : " + filename)

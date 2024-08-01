# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_sync
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from commen import openjson,existingpost
import json

class webScrapy:
    """
    爬虫模块：tor网络代理、爬虫、保存json数据
    """
    def __init__(self,ip='115.160.185.148',port=12908) -> None:
        """
        初始化，设置代理，读取数据表
        """
        self.ip = ip
        self.port = port
        self.proxy_path = "http://"+self.ip+":"+str(self.port)
        self.proxies = {
            'http':  'http://' + str(self.ip) + ':' + str(self.port),
            'https': 'https://' + str(self.ip) + ':' + str(self.port)
        } 
        self.sites = openjson('sites.json')
        self.posts = openjson('posts.json')
        self.pages = openjson('pages.json')

    def torBrowser(self,ip='127.0.0.1',port=9150):
        """
        将代理设置为torBrowser
        """
        self.ip = ip
        self.port = port
        self.proxy_path = "socks5://"+self.ip+":"+str(self.port)
        self.proxies = {
            'http':  'socks5h://' + str(self.ip) + ':' + str(self.port),
            'https': 'socks5h://' + str(self.ip) + ':' + str(self.port)
        } 

    def browser(self):
        """
        初始化playwright
        """
        try:
            self.play = sync_playwright().start()
            self.browser = self.play.chromium.launch(proxy={"server": self.proxy_path}, args=["--headless=new"])
        except:
            print("failed to launch playwright!")



    def scrape(self,site,post_url=""):
        """
        爬取网页，并将其添加到pages表中
        """
        url = post_url if post_url else site["url"]
        print("start scraping : " + site['label']['name'] + " : " + url)
        try:
            context = self.browser.new_context(ignore_https_errors= True)
            page = context.new_page()
            stealth_sync(page)

            try:
                page.goto(url, wait_until='domcontentloaded', timeout = 120000)
            except PlaywrightTimeoutError:
                print(f"Attempt  failed: Timeout while loading the page {site['url']}")
                return None
            except Exception as e:
                print(f"Attempt  failed: {e}")
                return None
            except:
                print("playwright fiald in page.goto")
                return None

            page.bring_to_front()
            page.wait_for_timeout(10000)
            page.mouse.move(x=500, y=400)
            page.wait_for_load_state('networkidle')
            page.mouse.wheel(delta_y=2000, delta_x=0)
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(10000)

            # 测试tor网络
            if "503 - Forwarding failure (Privoxy@localhost.localdomain)" == page.title():
                print(page.content())
                print("503 Error failed to get :" + site['url'])
                return None

            current_datetime = datetime.now()
            current_timestamp = current_datetime.timestamp()
            screenshots_name = 'screenshots/' + site['label']['name'] + '-' + str(current_timestamp) + '.png'
            page.screenshot(path=screenshots_name, full_page=True)
            image = Image.open(screenshots_name)
            
            # Format it in ISO format
            iso_formatted = current_datetime.isoformat()
            
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), iso_formatted, fill=(0, 0, 0))
            
            image.save(screenshots_name)
            
            # save page content
            filename = 'source/' + site['label']['name'] + '-' + str(current_timestamp) + '.html'
            with open(filename, 'w', encoding='utf-8') as sitesource:
                sitesource.write(page.content())
                sitesource.close()

            apage = {
                'platform' : site['label']['name'] ,
                'uuid' : str(current_timestamp),
                'crawl_time' : str(current_timestamp),
                'domain' : site['domain'],
                'content_encode' : None,
                'lang' : 'english',
                'meta' : None,
                'net_type' : 'tor',
                'page_source' : page.content(),
                'title' : page.title(),
                'url' : url,
                'images' : None,
                'publish_time' : str(current_timestamp),
                'subject' : '勒索',
                'content' : page.content(),
                'simhash_values' : None,
                'label' : {'type':'勒索','group_name':'group_name'},
                'threaten_level' : '中危',
                'snapshot' : None,
                'name' : screenshots_name,
                'path' : screenshots_name,
                'image_id' : None
            }

            self.pages.append(apage)

            with open("pages.json", "w", encoding='utf-8') as jsonfile:
                json.dump(self.pages, jsonfile, indent=4, ensure_ascii=False)

            return apage

        except:
            print("failed to get :" + site['url'])
            return None

    def close(self):
        """
        playwright运行完毕后关闭
        """
        self.browser.close()

    def appender(self,post_title="", group_name="", description="", website="", published="", post_url="",email="",price="",pay="", download="", country="",screenPath='', sourcePath=""):
        """
        将提取到的post添加到posts表中
        """
        post = {
            "platform" : group_name,
            "ransom_name" : group_name,
            "uuid" : None,
            "user_name" : group_name,
            "publish_time" : published,
            "content" : description,
            "url" : post_url,
            "title" : post_title,
            "crawl_time" : None,
            "source" : "tor",
            "images" : [],
            "attachments" : download,
            "email" : email,
            "bitcoin_addresses" : pay,
            "eth_addresses" : pay,
            "lang" : "english",
            "label" : {
                "country" : country,
                "victim" : website,
            },
            "extract_entity" : [],
            "threaten_level" : "中危"
        }
        if not existingpost(post,self.posts):
            self.posts.append(post)

            with open("posts.json", "w", encoding='utf-8') as jsonfile:
                json.dump(self.posts, jsonfile, indent=4, ensure_ascii=False)

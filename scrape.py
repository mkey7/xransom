# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_sync
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
import json

# tor网络的代理端口
#sockshost = '127.0.0.1'
#socksport = 9150
#proxy_path = "socks5://"+sockshost+":"+str(socksport)
sockshost = '115.160.185.148'
socksport = 12908
proxy_path = "http://"+sockshost+":"+str(socksport)

# socks5h:// ensures we route dns requests through the socks proxy
proxies = {
    'http':  'http://' + str(sockshost) + ':' + str(socksport),
    'https': 'https://' + str(sockshost) + ':' + str(socksport)
} 
# proxies = {
#     'http':  'socks5h://' + str(sockshost) + ':' + str(socksport),
#     'https': 'socks5h://' + str(sockshost) + ':' + str(socksport)
# }
class webScrapy:
    def __init__(self,ip='115.160.185.148',port=12908) -> None:
        self.ip = ip
        self.port = port
        self.proxy_path = "http://"+self.ip+":"+str(self.port)
        self.proxies = {
            'http':  'http://' + str(self.ip) + ':' + str(self.port),
            'https': 'https://' + str(self.ip) + ':' + str(self.port)
        } 

    def torBrowser(self,ip,port):
        self.ip = ip
        self.port = port
        self.proxy_path = "socks5://"+self.ip+":"+str(self.port)
        self.proxies = {
            'http':  'socks5://' + str(self.ip) + ':' + str(self.port),
            'https': 'socks5h://' + str(self.ip) + ':' + str(self.port)
        } 

    def browser(self):
        try:
            self.play = sync_playwright().start()
            self.browser = self.play.chromium.launch(proxy={"server": self.proxy_path}, args=["--headless=new"])
        except:
            print("failed to launch playwright!")

    def scrape(self,url,group_name):
        print("start scraping : " + group_name + " : " + url)
        context = self.browser.new_context(ignore_https_errors= True)
        page = context.new_page()
        stealth_sync(page)

        page.goto(url, wait_until='load', timeout = 120000)
        page.bring_to_front()
        page.wait_for_timeout(10000)
        page.mouse.move(x=500, y=400)
        page.wait_for_load_state('networkidle')
        page.mouse.wheel(delta_y=2000, delta_x=0)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(10000)

        # 保存快照
        current_datetime = datetime.now()
        current_timestamp = current_datetime.timestamp()
        name = 'screenshots/' + group_name + '-' + current_timestamp + '.png'
        page.screenshot(path=name, full_page=True)
        image = Image.open(name)
        
        # Format it in ISO format
        iso_formatted = current_datetime.isoformat()
        
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), iso_formatted, fill=(0, 0, 0))
        
        image.save(name)
        
        # save page content
        filename = 'source/' + group_name + '-' + current_timestamp + '.html'
        with open(name, 'w', encoding='utf-8') as sitesource:
            sitesource.write(page.content())
            sitesource.close()

        # TODO 转换成新的输出格�?
        return page.content()


# TODO 爬取网页，输出新的原始页面格式文件，并保存快照
def get_website(url,group_name,proxy_path = proxy_path):
    """
    对网页就行爬取，保存html文件和网页图片快照
    """
    with sync_playwright() as play:
        try:
            browser = play.chromium.launch(proxy={"server": proxy_path},
                args=['--unsafely-treat-insecure-origin-as-secure='+url, "--headless=new"])
            # 爬取html
            context = browser.new_context(ignore_https_errors= True)
            page = context.new_page()
            stealth_sync(page)
            page.goto(url, wait_until='load', timeout = 120000)
            page.bring_to_front()
            page.wait_for_timeout(10000)
            page.mouse.move(x=500, y=400)
            page.wait_for_load_state('networkidle')
            page.mouse.wheel(delta_y=2000, delta_x=0)
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(10000)

            # 保存快照
            current_datetime = datetime.now()
            name = 'screenshots/' + group_name + '-' + current_datetime + '.png'
            page.screenshot(path=name, full_page=True)
            image = Image.open(name)
            
            # Format it in ISO format
            iso_formatted = current_datetime.isoformat()
            
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), iso_formatted, fill=(0, 0, 0))
            
            image.save(name)
            
            # save page content
            filename = 'source/'+ group_name + '-' +current_datetime + '.html'
            with open(name, 'w', encoding='utf-8') as sitesource:
                sitesource.write(page.content())
                sitesource.close()

            # TODO 转换成新的输出格式

            return page.content()
        except PlaywrightTimeoutError:
            stdlog('Timeout!')
        except Exception as exception:
            errlog(exception)
        finally:
            browser.close()

if __name__ == "__main__":
    scrape = webScrapy()
    scrape.browser()
    content = scrape.scrape("https://www.baidu.com/","baidu")
    print(content)

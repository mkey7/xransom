# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_sync
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
import json

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
            'http':  'socks5h://' + str(self.ip) + ':' + str(self.port),
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
        try:
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

            # 真tor真真真真
            if "503 - Forwarding failure (Privoxy@localhost.localdomain)" == page.title():
                print(page.content())
                print("failed to get :" + url)
                return None

            current_datetime = datetime.now()
            current_timestamp = current_datetime.timestamp()
            name = 'screenshots/' + group_name + '-' + str(current_timestamp) + '.png'
            page.screenshot(path=name, full_page=True)
            image = Image.open(name)
            
            # Format it in ISO format
            iso_formatted = current_datetime.isoformat()
            
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), iso_formatted, fill=(0, 0, 0))
            
            image.save(name)
            
            # save page content
            filename = 'source/' + group_name + '-' + str(current_timestamp) + '.html'
            with open(filename, 'w', encoding='utf-8') as sitesource:
                sitesource.write(page.content())
                sitesource.close()

            return page.content()

        except:
            print("failed to get :" + url)
            return None

    def close(self):
        self.browser.close()

# NOTE 真
if __name__ == "__main__":
    scrape = webScrapy()
    scrape.browser()
    content = scrape.scrape("http://dkgn45pinr7nwvdaehemcrpgcjqf4fooit3c4gjw6dhzrp443ctvnoad.onion/leaks.html","mogilevich")
    print(content)
    scrape.close()

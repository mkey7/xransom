# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_sync
from datetime import datetime
import json
import hashlib  # sha1
import importlib
from bs4 import BeautifulSoup
import simhash
import minioUpdate
import MQ
import os
from dotenv import load_dotenv


class webScrapy:
    """
    爬虫模块：tor网络代理、爬虫、保存json数据
    """

    def __init__(self) -> None:
        """
        初始化，设置代理(socks5)，读取数据表
        """
        load_dotenv()

        self.ip = os.getenv('TOR_IP')
        self.port = os.getenv('TOR_PORT')

        # tor的代理
        socks = os.getenv('TOR_SOCKS5')
        if socks:
            self.proxy_path = "socks5://"+self.ip+":"+str(self.port)
            self.proxies = {
                'http':  'socks5h://' + str(self.ip) + ':' + str(self.port),
                'https': 'socks5h://' + str(self.ip) + ':' + str(self.port)
            }
        else:
            self.proxy_path = "http://"+self.ip+":"+str(self.port)
            self.proxies = {
                'http':  'http://' + str(self.ip) + ':' + str(self.port),
                'https': 'https://' + str(self.ip) + ':' + str(self.port)
            }

        self.mq = MQ.mqClient()

        self.minio = minioUpdate.minioClient()

        self.sites = self.openjson('sites.json')
        self.posts = self.openjson('posts.json')
        self.pages = self.openjson('pages.json')
        self.users = self.openjson('users.json')
        self.cont = 0

    def browserInit(self):
        """
        初始化playwright
        """
        try:
            self.play = sync_playwright().start()
            # self.browser = self.play.chromium.launch(
            self.browser = self.play.firefox.launch(
                proxy={"server": self.proxy_path},
                args=["--headless=new"]
            )
            print(f"browser init! Tor: {self.proxy_path}")
        except Exception as e:
            print(f"failed to launch playwright! {e}")

    def scrape(self, site, post_url=""):
        """
        爬取网页，并将截图保存到screenshot中，但是抓到的网页并不保存至page.json中
        """
        self.cont += 1
        if self.cont % 5 == 0:
            print(f"xransom has try to crawl {self.cont} pages")
            self.close()
            self.browserInit()

        url = post_url if post_url else site["url"]
        print("start scraping : " + site['label']['name'] + " : " + url)

        try:
            context = self.browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            stealth_sync(page)
            page.set_viewport_size({"width": 1280, "height": 5000})

            try:
                response = page.goto(url, wait_until='load',
                                     timeout=120000)
                http_status_code = str(response.status)  # 获取页面状态码

            except PlaywrightTimeoutError:
                print(f"Attempt  failed: Timeout while loading the page \
                {site['url']}")
                return None
            except Exception as e:
                print(f"Attempt  failed: {e}")
                return None

            # 测试tor网络
            if http_status_code[0] == "4":
                print("404 Error to get :" + site['url'])
                return None

            page.bring_to_front()
            page.wait_for_timeout(15000)
            page.mouse.move(x=500, y=400)
            page.wait_for_load_state('networkidle')
            page.mouse.wheel(delta_y=2000, delta_x=0)
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(15000)

            # uuid
            e = url+page.title()
            sha1_value = self.calculate_sha1(e)

            current_datetime = datetime.now()
            current_timestamp = current_datetime.timestamp()

            # 获取截图
            screenshots = self.get_screenshot(page, sha1_value,
                                              site['label']['name'])

            text, meta_str, encoding = self.get_soup(page)

            # simhash
            hash1 = simhash.Simhash(text.split()).value

            apage = {
                'platform': site['label']['name'],
                'uuid': sha1_value,
                'crawl_time': str(current_timestamp),
                'domain': site['domain'],
                'content_encode': encoding,
                'lang': 'english',
                'meta': meta_str,
                'net_type': 'tor',
                'page_source': page.content(),
                'title': page.title(),
                'url': url,
                'images': [],
                'publish_time': str(current_timestamp),
                'subject': '勒索',
                'content': text,
                'simhash_values': hash1,
                'label': {
                    'type': '勒索',
                    'group_name': site["label"]["name"]
                },
                'threaten_level': '中危',
                'snapshot': screenshots
            }

            page.close()
            context.close()

            # self.existingpage(apage)
            self.mq.mqSend(apage, 'page')
            return apage

        except Exception as e:
            print(f"ERROR: failed to get page:{url}, because of  {e}")
            return None

    def close(self):
        """
        playwright运行完毕后关闭
        """
        if hasattr(self, 'browser') and self.browser:
            self.browser.close()
        if hasattr(self, 'play') and self.play:
            self.play.stop()
        print("playwright closed!")
        # self.writejson("pages.json", self.pages)
        # self.writejson("posts.json", self.posts)
        print("write pages and posts to json!")

    def run(self, group_name):
        """
        爬取指定组织的网站并调用解析模块实行解析
        """
        for site in self.sites:
            if site["label"]["name"] != group_name:
                continue

            page = self.scrape(site)

            if not page:
                # 更新site
                site["last_status"] = False
                site["is_recent_online"] = False
                self.writejson("sites.json", self.sites)
                continue

            # 调用解析模块
            self.parser(group_name, page, site)

            # 更新site
            # 转换为 datetime 对象
            dt_object = datetime.utcfromtimestamp(float(page["publish_time"]))
            last_publish_time = dt_object.strftime('%Y-%m-%d %H:%M:%S.%f')

            site["last_publish_time"] = last_publish_time
            if site["first_publish_time"] == "":
                site["first_publish_time"] = site["last_publish_time"]
            site["last_status"] = True
            site["is_recent_online"] = True
            site["snapshot"] = page["snapshot"]
            self.writejson("sites.json", self.sites)
            self.mq.mqSend(site, 'site')

            # 更新user
            for user in self.users:
                if user["platform"] == group_name:
                    user["last_active_time"] = page["publish_time"]
                    user["crawl_time"] = page["publish_time"]
                    if user["register_time"] == "":
                        user["register_time"] = page["publish_time"]
            self.writejson("users.json", self.users)
            self.mq.mqSend(user, 'user')

    def parser(self, group_name, page, site):
        """
        调用对应勒索组织的解析模块
        """
        parse_name = f"parsers.{group_name}"

        try:
            module = importlib.import_module(parse_name)
            module.main(self, page, site)
        except ModuleNotFoundError:
            print(f"No script found for organization: {parse_name}")
        except AttributeError:
            print(f"The script for organization: {parse_name} does not have a \
                main function.")

    def appender(self, post_title="", group_name="", content="",
                 website="", published="", post_url="", email="",
                 download=[], country="", btc="", eth="", price="",
                 industry="", images=[], page=None):
        """
        将提取到的post添加到posts表中
        """
        # uuid
        e = group_name + post_title
        uuid = self.calculate_sha1(e)
        user_id = self.calculate_sha1(group_name)

        post = {
            "platform": group_name,
            "ransom_name": group_name,
            "uuid": uuid,
            "user_id": user_id,
            "user_name": group_name,
            "publish_time": published if published else page["publish_time"],
            "content": content,
            "url": post_url,
            "title": post_title,
            "crawl_time": page["crawl_time"],
            "source": "tor",
            "images": images,
            "attachments": download,
            "email": email,
            "bitcoin_addresses": btc,
            "eth_addresses": eth,
            "lang": "english",
            "label": {
                "country": country,
                "victim": website,
                "pageid": page["uuid"] if page else None,
                "price": price,
                "industry": industry,
            },
            "extract_entity": [],
            "threaten_level": "中危"
        }

        # self.existingpost(post)
        self.mq.mqSend(post, 'ransom')

    def existingpost(self, post):
        '''
        check if a post already exists in posts.json
        '''
        for p in self.posts:
            if p['uuid'] == post["uuid"]:
                print('post already exists: ' + post["title"])
                post["publish_time"] = p["publish_time"]
                p = post
                return True
        print('post does not exist: ' + post["title"])
        self.posts.append(post)
        return False

    def existingpage(self, page):
        '''
        check if a page already exists in pages.json
        '''
        for p in self.pages:
            if p['uuid'] == page["uuid"]:
                print('page already exists: ' + page["title"])
                p = page
                return True
        print('page does not exist: ' + page["title"])
        new_page = {k: v for k, v in page.items() if k != 'page_source'}
        self.pages.append(new_page)
        return False

    def openjson(self, file):
        '''
        opens a file and returns the json as a dict
        '''
        with open(file, encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
        return data

    def writejson(self, file, data):
        '''
        opens a file and write the json to a json file
        '''
        with open(file, "w", encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4, ensure_ascii=False)
            jsonfile.truncate()

    def calculate_sha1(self, data):
        # 创建一个新的sha1 hash对象
        hash_object = hashlib.sha1()
        # 提供需要散列的数据
        hash_object.update(data.encode())
        # 获取十六进制格式的散列值
        return hash_object.hexdigest()

    def get_screenshot(self, page, sha1_value, siteName, section_height=2000):
        """
        抓取网页截图
        """
        screenshots = []
        try:
            screenshot_path = f'screenshots/{sha1_value}.png'

            page.screenshot(path=screenshot_path, full_page=True)

            screenshot = {
                'name': f'{sha1_value}.png',
                'path': 'screenshots/',
                'image_id': f'{sha1_value}',
            }
            screenshots.append(screenshot)

        except Exception as e:
            print(f"ERROR screenshot: {e}")
            # NOTE 分段截图
            total_height = page.evaluate("document.body.scrollHeight")
            viewport_width = page.viewport_size["width"]

            for i in range(0, total_height, section_height):
                clip_area = {"x": 0, "y": i, "width": viewport_width,
                             "height": min(section_height, total_height - i)}

                # 如果超出页面范围则跳过截图
                if clip_area["height"] <= 0:
                    continue

                # 截取当前部分的截图
                screenshot_path = f'screenshots/{sha1_value}-{i/section_height}.png'

                page.screenshot(path=screenshot_path, clip=clip_area,
                                full_page=False)

                screenshot = {
                    'name': f'{sha1_value}-{i/section_height}.png',
                    'path': siteName,
                    'image_id': f'{sha1_value}-{i/section_height}',
                }
                screenshots.append(screenshot)

        finally:
            for screenshot in screenshots:
                minioPath = siteName + "/" + screenshot["name"]
                screenshot_path =  "screenshots/" + screenshot["name"]
                self.minio.upload_to_minio(screenshot_path, minioPath, "xransoms")
            return screenshots

    def get_soup(self, page):
        """
        从html网页中提取相关内容
        """
        # content
        soup = BeautifulSoup(page.content(), 'html.parser')
        text = soup.get_text()

        # meta
        metas = soup.find_all('meta')
        meta_str = ""
        for meta in metas:
            meta_str += str(meta) + '\n'

        # 查找带有charset的meta标签
        encoding = ""
        meta_charset = soup.find('meta', charset=True)
        if meta_charset:
            encoding = meta_charset['charset']

        # 查找带有Content-Type的meta标签
        meta_content_type = soup.find('meta', attrs={
            'http-equiv': 'Content-Type'})
        if meta_content_type and 'charset' in meta_content_type['content']:
            content_type = meta_content_type['content']
            encoding = content_type.split('charset=')[-1]

        return text, meta_str, encoding

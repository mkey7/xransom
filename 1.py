import scrape
import importlib
import json

print("start xransom!")

scrapy = scrape.webScrapy()
scrapy.torBrowser()
scrapy.browser()

site_string = """
{
        "uuid": 10138,
        "net_type": "tor",
        "description": "",
        "lang": "english",
        "service_type": "勒索",
        "label": {
            "type": "勒索",
            "name": "dunghill"
        },
        "site_hazard": "高危",
        "scale": 1,
        "active_level": 1,
        "domain": "p66slxmtum2ox4jpayco6ai3qfehd5urgrs4oximjzklxcol264driqd.onion",
        "url": "http://p66slxmtum2ox4jpayco6ai3qfehd5urgrs4oximjzklxcol264driqd.onion/index.html",
        "title": "Dunghill Leak - Details",
        "snapshot": "",
        "path": "",
        "name": "",
        "image_id": "",
        "last_status": true,
        "first_publish_time": "2024-07-02 13:01:26.409777",
        "last_publish_time": "2024-07-02 13:01:26.409745",
        "is_recent_online": true,
        "goods_label": "勒索",
        "goods_count": 0,
        "pay_methods": "btc",
        "goods_user_count": 0
    }
"""

site = json.loads(site_string)

page = scrapy.scrape(site)
if not page:
    print("failed")

if not page:
    exit()
print(page)
group_name = page["platform"]
parse_name = f"parsers.{group_name}"

try:
    module = importlib.import_module(parse_name)
    module.main(scrapy,page,site)
except ModuleNotFoundError:
    print(f"No script found for organization: {parse_name}")
except AttributeError:
    print(f"The script for organization: {parse_name} does not have a main function.")

scrapy.close()

import scrape
import os
import importlib

print("start xransom!")

scrapy = scrape.webScrapy()
scrapy.torBrowser()
scrapy.browser()

for site in scrapy.sites:
    page = scrapy.scrape(site)
    if not page:
        continue

        # 将文件路径转换为模块名称
    
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

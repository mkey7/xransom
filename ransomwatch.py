import scrape
import os
import importlib

<<<<<<< HEAD
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
=======
if __name__ == "__main__":

    print("start xransom!")

    scrapy = scrape.webScrapy()
    scrapy.socks()
    scrapy.browserInit()

    directory = "parsers/"
    files_and_dirs = os.listdir(directory)

    for name in files_and_dirs:
        if name[0:2] == "__":
            continue
        scrapy.run(name[0:-3])

    scrapy.close()
>>>>>>> 326597d (parser)

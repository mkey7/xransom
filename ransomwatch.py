from commen import openjson
import scrape

print("start xransom!")

scrapy = scrape.webScrapy()

for site in scrapy.sites:
    print(site['url'])
    print(site['label']['name'])

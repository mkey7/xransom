from commen import openjson
import scrape

print("start xransom!")

scrapy = scrape.webScrapy()
scrapy.torBrowser()
scrapy.browser()

for site in scrapy.sites:
    scrapy.scrape(site)
    
scrapy.close()

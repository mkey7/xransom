import scrape

if __name__ == "__main__":

    print("start xransom!")

    scrapy = scrape.webScrapy()
    # scrapy.torHttp()
    scrapy.browser()

    name = ""
    scrapy.run(name)

    scrapy.close()

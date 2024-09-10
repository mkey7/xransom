import scrape

if __name__ == "__main__":

    print("start xransom!")

    scrapy = scrape.webScrapy()
    # scrapy.torHttp()
    scrapy.browserInit()

    name = "0mega"
    scrapy.run(name)

    scrapy.close()

import scrape

if __name__ == "__main__":

    print("start xransom!")

    scrapy = scrape.webScrapy()
    scrapy.browserInit()

    name = "play"
    scrapy.run(name)

    scrapy.close()

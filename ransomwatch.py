import scrape
import os

if __name__ == "__main__":

    print("start xransom!")

    scrapy = scrape.webScrapy()
    scrapy.browserInit()

    directory = "parsers/"
    files_and_dirs = os.listdir(directory)

    for name in files_and_dirs:
        if name[0:2] == "__":
            continue
        scrapy.run(name[0:-3])

    scrapy.close()

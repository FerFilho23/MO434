import scrapy
import os
from datetime import date

class ExtractTexts(scrapy.Spider):
    name   = "extract_texts"

    # Creates a folder named by the current date and yields the urls
    
    def start_requests(self):
        folder = date.today()
        os.system("mkdir {}".format(folder))
        with open('links.csv', 'r') as file:
            for line in file:
                url = line.strip()
                yield scrapy.Request(url=url, callback=self.parse)
            file.close()

    # parse the texts from those urls into html files inside that folder. 
    
    def parse(self, response):
        folder = date.today()
        page = response.url.split("/")[-2]
        filename = "{}/{}.html".format(folder,page)
        with open(filename, 'wb') as file:
            file.write(response.body)
            file.close()

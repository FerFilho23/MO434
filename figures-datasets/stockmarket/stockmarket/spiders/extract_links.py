import scrapy
import csv

class ExtractLinks(scrapy.Spider):
    name     = "extract_links" 
    maxdepth = 1 # crawling depth from initial urls
    
    # provide the list of urls
    
    def start_requests(self):
        urls = [
            'https://finance.yahoo.com/topic/stock-market-news/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # define the parse function that will create 
    # a list of urls from the initial ones provided above.
    
    def parse(self, response):
        """ Main function that parses downloaded pages """
        # Save link
        if (response.url.split(".")[-1] == "html"): 
            with open('links.csv', 'a', newline='') as file:
                writer = csv.writer(file)            
                writer.writerow([response.url])
                file.close()
        # Get all the <a> tags
        a_selectors = response.xpath("//a")
        # Loop on each tag
        for depth in range(self.maxdepth):
            for selector in a_selectors:
                # Extract the link text
                text = selector.xpath("text()").extract_first()
                # Extract the link href
                link = selector.xpath("@href").extract_first()
                # Create a new Request object
                request = response.follow(link, callback=self.parse)
                # Return it thanks to a generator
                yield request            

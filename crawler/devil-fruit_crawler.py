import scrapy

class OnePieceSpider(scrapy.Spider):
    name = 'onepiecespider'
    start_urls = ['https://onepiece.fandom.com/wiki/Category:Devil_Fruits']

    categories = ['Paramecia', 'Logia', 'Zoan']    

    def parse(self, response):
        for href in response.css('.category-page__members')[0].css("a::attr(href)").extract():
            lastIndex = len(href.split(":")) - 1
            
            if href.split(":")[lastIndex] in categories:
                extracted_data = scrapy.Request("https://onepiece.fandom.com" + href, callback=self.parse_categories_devil_fruit)
                
                yield extracted_data
                
    def parse_categories_devil_fruit(self, response):
        for href in response.css(".category-page__members")[0].css("a::attr(href)").extract():
            if len(href.split(":")) == 1:
                extracted_data = scrapy.Request("https://onepiece.fandom.com" + href, callback=self.parse_devil_fruit)
                
                yield extracted_data        
    
    def parse_devil_fruit(self, response):
        devil_fruit_name = response.css("span.mw-page-title-main").extract()[0].strip()
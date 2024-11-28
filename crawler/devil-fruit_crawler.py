import scrapy
from bs4 import BeautifulSoup


class OnePieceSpider(scrapy.Spider):
    name = 'onepiecespider'
    start_urls = ['https://onepiece.fandom.com/wiki/Category:Devil_Fruits']

    categories = ['Paramecia', 'Logia', 'Zoan']    

    def parse(self, response):
        for href in response.css('.category-page__members')[0].css("a::attr(href)").extract():
            lastIndex = len(href.split(":")) - 1
            
            if href.split(":")[lastIndex] in self.categories:
                extracted_data = scrapy.Request("https://onepiece.fandom.com" + href, callback=self.parse_categories_devil_fruit)
                
                yield extracted_data
                
    def parse_categories_devil_fruit(self, response):
        for href in response.css(".category-page__members")[0].css("a::attr(href)").extract():
            if len(href.split(":")) == 1:
                extracted_data = scrapy.Request("https://onepiece.fandom.com" + href, callback=self.parse_devil_fruit)
                
                yield extracted_data        
    
    def parse_devil_fruit(self, response):
        devil_fruit_name = response.css("span.mw-page-title-main").extract()[0].strip()
        
        div_selector = response.css("div.mw-parser-output")[0]
        div_html = div_selector.extract()
        
        soup = BeautifulSoup(div_html).find('div')
        
        devil_fruit_type=""
        
        if soup.find('aside'):
            aside = soup.find('aside')
            
            for cell in aside.find_all('div', {'class': 'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name == 'Type:':
                        devil_fruit_type = cell.find('div').text.strip().split("[")[0]
                        
        soup.find('aside').decompose()
        
        devil_fruit_description = soup.text.strip()
        devil_fruit_description = devil_fruit_description.split('Trivia')[0].strip()
        
        return dict (
            devil_fruit_name = devil_fruit_name,
            devil_fruit_type = devil_fruit_type,
            devil_fruit_description = devil_fruit_description 
        )
        
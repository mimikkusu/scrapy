from gc import callbacks
from pip import main
import scrapy

class BooksBasicSpider(scrapy.Spider):
    name = 'books_basic'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    def parse(self, response):
        books = response.xpath('//h3')
        for book in books:    
            # title = book.xpath('.//a/text()').get()
            # link = book.xpath('.//a/@href').get()
            # yield{
            #   'title':title,
            #   'URL':link        
            #   }
            yield response.follow(url = book.xpath(".//a/@href").get(),callback=self.parse_items)
            
        next_pages = response.xpath("//li[@class='next']/a/@href").get()  
        if next_pages:
          yield response.follow(url=next_pages,callback=self.parse)
          
    def parse_items(self,response):
      main_book_info = response.xpath('//div[@class="col-sm-6 product_main"]')
      title = main_book_info.xpath('.//h1/text()').get()
      price = main_book_info.xpath('.//p[@class="price_color"]/text()').get()
      rating = main_book_info.xpath('.//p[3]/@class').get()
      cpu = response.xpath('//th[contains(text(),"UPC")]/following-sibling::td/text()').get()
      review = response.xpath('//th[contains(text(),"Number of review")]/following-sibling::td/text()').get()
      yield{
       'title':title,
       'price':price,
       'rating':rating,
       'cpu':cpu,
       'review':review 
      }
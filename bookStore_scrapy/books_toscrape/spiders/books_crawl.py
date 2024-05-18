import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksCrawlSpider(CrawlSpider):
    name = 'books_crawl'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3/a'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a'),follow=True)
    )

    def parse_item(self, response):
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

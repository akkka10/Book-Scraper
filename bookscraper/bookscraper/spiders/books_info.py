import scrapy
from bookscraper.items import BookItem
from bookscraper.items import BookItem
class BooksInfoSpider(scrapy.Spider):
    name = "books_info"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books=response.css("article.product_pod")
        for book in books:
            book_url=book.css("div.image_container a::attr(href)").get()
    
            yield response.follow(book_url,callback=self.parse_book)
        next_page=response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page,callback=self.parse)
        
    def parse_book(self,response):
        table=response.css("table tr ")
        book_item=BookItem()
        
        book_item['title']=response.xpath("//div[contains(@class,'product_main')]/h1/text()").get()
        book_item[ 'prod_description']=response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['category']=response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['product_type']=table[1].css("td::text").get()
        book_item['price_exc_tax']=table[2].css("td::text").get()
        book_item['price_inc_tax']=table[3].css("td::text").get()
        book_item['tax']=table[4].css("td::text").get()
        book_item['availability']=table[5].css("td::text").get()
        book_item['num_reviews']=table[6].css("td::text").get()
        book_item['price']=response.css("p.price_color::text").get()
        book_item['rating']=response.css("p.star-rating::attr(class)").get().replace("star-rating","").strip()
        
        yield book_item



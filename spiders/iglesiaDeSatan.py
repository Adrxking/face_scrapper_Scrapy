import scrapy


class IglesiadesatanSpider(scrapy.Spider):
    name = 'iglesiaDeSatan'
    allowed_domains = ['iglesiadesatan.com']
    start_urls = ['https://iglesiadesatan.com/blog/']

    def parse(self, response):
        posts = response.css('article.post')
        for post in posts:
            href = post.css('.post-thumb-img-content.post-thumb > a::attr(href)').get()
            print('href', href)
            yield scrapy.Request(href, callback = self.parse_post, meta={'href': href})
        next_page = response.css('.next.page-numbers')
        print(next_page)
        if next_page:
            next_href = next_page.css('::attr(href)').get()
            yield scrapy.Request(next_href)
        
    def parse_post(self, response):
      href = response.meta.get('href')
      print(href)
      element = response.css('.post-thumb-img-content.post-thumb')
      print(element)
      img = element.css('img::attr(src)').get()
      yield {
        'href': href,
        'img': img
      }

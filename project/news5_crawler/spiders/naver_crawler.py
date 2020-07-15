import scrapy

from naver_crawler.items import NaverCrawlerItem

class NaverSpider(scrapy.Spider):
     name = "naver"

    def start_requests(self):

      start_date = (datetime.date(2020,7,11)).strftime('%Y.%m.%d')
      end_date = (datetime.date(2020,7,12)).strftime('%Y.%m.%d')
      start_page=1
      
      while True:
        
        start_url = "https://search.naver.com/search.naver?&where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=3&ds={0}&de={1}&docid=&nso=so:dd,p:,a:all&mynews=1&start={2}&refresh_start=0".format(start_date, end_date,start_page)
        
       
        if start_url.xpath('div[@class="paging"]/a[@class="next"]/text()'):
          start_page += 10
          
          yield scrapy.Request(start_url,self.parse_url)
        else:
          yield scrapy.Request(start_url,self.parse_url)
          break

    def parse_url(self, response):
        urls = response.xpath('//*/dl/dd[1]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_page_contents)

    def parse_page_contents(self,response):
        item = NaverCrawlerItem()
        item['title'] = response.xpath('//*[@id="articleTitle"]/text()').extract()
        item['article'] = response.xpath('//*[@id="articleBodyContents"]').extract()
        yield item

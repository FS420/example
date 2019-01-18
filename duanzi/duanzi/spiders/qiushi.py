import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
class QiushiSpider(RedisCrawlSpider):
    name = 'qiushi'
    allowed_domains = ['qiushibaike.com']
    # start_urls = ['https://www.qiushibaike.com/text/page/1/']
    start_urls="qiushi:start_urls"
    index = 1
    rules = (
        # 在每个页面寻找符合以下正则的链接，请求链接，获得parse_item中的查找内容
        Rule(LinkExtractor(allow=r'/article/\d+'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'/text/page/\d+/'), callback='parse_item', follow=True),
        # 不需要callback, 上面那个需要callback，在详细中拿出人名和内容
        Rule(LinkExtractor(allow=r'/text/page/\d+/'), follow=True),
    )
    def parse_item(self, response):
        # 详细页面(/article/\d+)里面又有f符合条件的(/article/\d+)
        name = response.xpath("//span[@class='side-user-name']/text()").extract_first()
        content = response.xpath("//div[@class='content']/text()").extract_first()
        if name != None or content != None:
            print(self.index)
            self.index = self.index
            return {             # 自动存储到redis中
                "name":name,
                "content":content
            }
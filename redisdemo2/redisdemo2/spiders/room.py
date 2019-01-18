import scrapy
from scrapy_redis.spiders import RedisSpider
class RoomSpider(RedisSpider):
    name = 'room'
    allowed_domains = ['lianjia.com']
    # 从redis队列中读取url,根据redis_key获取url
    redis_key = "lianjia:start_urls"
    # 页码
    index = 2
    base_url = "https://zj.lianjia.com/ershoufang/pg{}/"
    def parse(self, response):
        # 一页的25个 xiaoqus  prices  per_matters
        # 地址
        xiaoqus = response.xpath("//a[@class='no_resblock_a']/text()").extract()
        # 总价
        price_selectors  = response.xpath("//div[@class='totalPrice']")
        prices = []
        for price in price_selectors:
            prices.append(price.xpath("string(.)").extract_first())
        # 每平方的价格
        per_matters = response.xpath("//div[@class='unitPrice']/span/text()").extract()
        # 详细url
        detail_urls = response.xpath("//div[@class='title']/a/@href").extract()
        print(len(detail_urls))
        print(len(xiaoqus))
        print(len(prices))
        print(len(per_matters))
        for xiaoqu,price,per_matter,url in zip(xiaoqus,prices,per_matters,detail_urls):
            item = {}
            item["xiaoqu"] = xiaoqu
            item["price"] = price
            item["per_matter"] = per_matter
            print(url)
            # 请求每个二手房的详细url
            yield scrapy.Request(url,callback=self.detail_info,meta={"item":item})

        # 因为连接网获取不到页码url,所有通过这个方法发起对每一页的请求
        if self.index < 10:
            yield scrapy.Request(self.base_url.format(self.index),callback=self.parse)
        self.index = self.index+1

    # 处理详细信息
    def detail_info(self,response):
        print("哈哈哈哈")
        item = response.request.meta.get("item")
        # 几室几厅 3室2厅
        room_num = response.xpath("//div[@class='room']/div[@class='mainInfo']/text()").extract_first()
        item["room_num"]=room_num
        # 方向    南
        direction = response.xpath("//div[@class='type']/div[@class='mainInfo']/text()").extract_first()
        item["direction"] = direction
        # 多大平方 132.5
        occupation = response.xpath("//div[@class='area']/div[@class='mainInfo']/text()").extract_first()
        item["occupation"] = occupation
        # 地区   润州 润州
        area = response.xpath("string(//span[@class='info'])").extract_first()
        item["area"] = area
        # 楼层  中楼层 共17层
        lou_ceng = response.xpath("//div[@class='base']/div[@class='content']//li[2]/text()").extract_first()
        item["lou_ceng"] = lou_ceng
        # 梯户 一梯一户
        tihu = response.xpath("//div[@class='base']/div[@class='content']//li[last()-2]/text()").extract_first()
        item["tihu"] = tihu
        # 是否有电梯
        dianti = response.xpath("//div[@class='base']/div[@class='content']//li[last()-1]/text()").extract_first()
        item["dianti"] = dianti
        # 产权 70年
        time = response.xpath("//div[@class='base']/div[@class='content']//li[last()]/text()").extract_first()
        item["time"] = time
        # 交易权属 商品房
        jiaoyi = response.xpath("string(//div[@class='transaction']/div[@class='content']//li[2]/span[2])").extract_first().strip()
        item["jiaoyi"] = jiaoyi
        # 房屋用途 普通房
        yongtu = response.xpath("string(//div[@class='transaction']/div[@class='content']//li[4]/span[2])").extract_first().strip()
        item["yongtu"] = yongtu
        yield item

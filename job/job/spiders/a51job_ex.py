# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
class A51jobExSpider(scrapy.Spider):
    name = '51job_ex'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/070300,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self, response):
        link1 = LinkExtractor(allow=r'suzhou.*/\d+.html')
        link2  = LinkExtractor(allow=r'list\S+fare=')
        info_a = link1.extract_links(response)
        page_a = link2.extract_links(response)
        print(len(info_a))
        print(len(page_a))
        for info in info_a:
            print(info)
        for page in page_a:
            print(page)

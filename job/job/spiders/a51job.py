import scrapy,re,json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
class A51jobSpider(CrawlSpider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/070300,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']
    rules = (
        # 按照这个规则获得所有的完整链接，这个获得职位的链接
        Rule(LinkExtractor(allow=r'suzhou.*/\d+.html'), callback='parse_item', follow=True),
        # 这个获得所有的页码
        Rule(LinkExtractor(allow=r'list\S+fare='),follow=True),
    )
    def parse_item(self, response):
        # 职位名称
        title = response.xpath("//h1/text()").extract_first().strip()
        # 公司名称
        company_name = response.xpath("//a[@class='catn']/text()").extract_first().strip()
        # 工资 0.8-1.5万/月   4-6千/月   1.5千以下/月
        min_salary ,max_salary = self.parse_salary(response)
        # 要求  苏州  |  无工作经验  |  本科  |  招2人  |  12-18发布  |  英语良好  |  电子信息科学与技术 光信息科学与技术申请职位竞争力分析
        # 公司地区 经验 学历 招人数 发布时间
        address, experience, education, employ_num, publish = self.parse_company_info(response)
        min_experience,max_experience = self.parse_experience(experience)
        # 上班详细地点
        work_place = ""
        work_selector = response.xpath("//div[@class='bmsg inbox']/p[@class='fp']/text()")
        if len(work_selector)>0:
            work_place =work_selector[1].get().strip()

        # 职能类型
        type = response.xpath("//p[@class='fp'][1]/a/text()").extract_first().strip()
        # 关键字
        key_list = response.xpath("//p[@class='fp'][2]/a/text()")
        key_word=""
        if len(key_list) > 0:
            key_word = key_list.extract_first().strip()
        # 要双引号
        yield {
            "title":title,
            "company_name":company_name,
            "min_salary":min_salary,
            "max_salary":max_salary,
            "address":address,
            "min_experience":min_experience,
            "max_experience":max_experience,
            "education":education,
            "employ_num":employ_num,
            "publish":publish,
            "work_place":work_place,
            "type":type,
            "key_word":key_word
        }
    # 工作经验的处理
    def parse_experience(self,experience):
        if experience=="无工作经验":
            return 0,0
        elif experience.find("-")!=-1:   # 3-4年经验
            min_experience,max_experience = re.findall("(\d+)-(\d+)",experience)[0]
        else:  # 3年经验
            min_experience = re.findall("(\d+)",experience)[0]
            max_experience = min_experience
        return min_experience,max_experience

    def parse_company_info(self,response):
        info_list = response.xpath("//p[@class='msg ltype']/text()").extract()
        # 地址
        address = info_list[0].strip()
        # 工作经验 无工作经验 5-7工作经验
        experience = info_list[1].strip()
        # 学历  大专 本科 硕士
        education = ""
        # 招人数
        employ_num = 0
        # 发布时间
        publish = ""
        # 没有学历
        if info_list[2].find("大专")!=-1 or info_list[2].find("本科")!=-1 or info_list[2].find("硕士")!=-1 :
            education = info_list[2].strip()
            employ_num = info_list[3].strip()
            publish = info_list[4].strip()
        else:
            employ_num = info_list[2].strip()
            publish = info_list[3].strip()
        return address,experience,education,employ_num,publish

    # 工资的处理
    def parse_salary(self,response):
        salary = response.xpath("//div[@class='cn']/strong/text()").extract_first()
        if salary == None:
            return 0,0
        salary = salary.strip()

        if salary.find("-") != -1:
            if salary.find("万") != -1:
                min_salary,max_salary = re.findall("(\S+)-(\S+)万",salary)[0]
                min_salary = float(min_salary)*10
                max_salary = float(max_salary)*10
            elif salary.find("千")!= -1:
                min_salary, max_salary = re.findall("(\S+)-(\S+)千", salary)[0]
                min_salary = float(min_salary)
                max_salary = float(max_salary)
        else:
            if salary.find("万") != -1:
                max_salary = re.findall("(\S+)万", salary)[0]
                max_salary = float(max_salary)*10
                min_salary = max_salary
            else:
                max_salary = re.findall("(\S+)千", salary)[0]
                max_salary = float(max_salary)
                min_salary = max_salary
        return min_salary,max_salary


from pymysql import connect
class JobPipeline(object):
    def open_spider(self,spider):
        # pymsql数据库连接方式
        self.client = connect(host="localhost",port=3306,user="root",password="123456",db="job",charset="utf8")
        self.cursor = self.client.cursor()
    def process_item(self, item, spider):
        sql="insert into job52 VALUES(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,[
                    item["title"],
                    item["company_name"],
                    item["min_salary"],
                    item["max_salary"],
                    item["address"],
                    item["min_experience"],
                    item["max_experience"],
                    item["education"],
                    item["employ_num"],
                    item["publish"],
                    item["work_place"],
                    item["type"],
                    item["key_word"]
        ])
        self.client.commit()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.client.close()


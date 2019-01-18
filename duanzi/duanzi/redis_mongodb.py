import pymongo
import json,redis
redis = redis.Redis(host="localhost",port=6379,db=0)
clicent = pymongo.MongoClient()
collection = clicent.qiushi.duanzi
while True:
    # 这只是取一个记录
    key, data = redis.blpop(["qiushi:items"])
    print(key)
    d = json.loads(data)
    print(d)
    collection.insert_one(d)




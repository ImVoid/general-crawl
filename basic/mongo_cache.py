# --coding:utf-8 --

from datetime import datetime, timedelta
from pymongo import MongoClient

class MongoCache:
    """
    数据库缓存
    MongoDB的过期删除操作是每分钟检测的，所以过期时间少于1分钟是无效的
    """
    def __init__(self, client=None, expires=timedelta(days=30)):
        # 如果未传递client参数，将尝试链接本地DB
        self.client = MongoClient('localhost', 27017) if client is None else client
        # 创建库
        self.db = self.client.cache
        # 设置数据过期时间, 数据过期后MongoDB会自动删除数据
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    # 以url为线索从DB获取数据
    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id':url})
        if record:
            return record['result']
        else:
            raise KeyError(url + ' does not exist')

    # 以url为线索从DB存储数据
    def __setitem__(self, url, result):
        record = {'result': result, 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)
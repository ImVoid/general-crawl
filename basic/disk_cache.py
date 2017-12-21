# --coding:utf-8--

import re
import os
import zlib
import urlparse
import pickle
from datetime import datetime, timedelta

class DiskCache:
    """利用文件系统缓存,并设置过期时间为30天
        此缓存可能存在重复key，但value不同的情况
        故不应在生产环境使用
        如有必要请改造key为hash
    """
    def __init__(self, cache_dir='cache', expires=timedelta(days=30)):
        self.cache_dir = cache_dir
        self.expires = expires

    # 将url映射为文件路径
    def url_to_path(self, url):
        # 分割url的不同部分
        components = urlparse.urlparse(url)
        # 为空path & “/”结尾的url添加index.data后缀
        path = components.path
        if not path:
            path = '/index'
        elif path.endswith('/'):
            path += 'index'
        # 为所有文件命添加后缀.data,避免出现index文件名和index文件夹在同一目录
        filename = components.netloc + path + components.query + '.data'
        # 替换文件系统不合法字符
        filename = re.sub('[^/0-9a-zA-Z\-.,;]', '_', filename)
        # 每个文件夹名长度不能超出255
        filename = "/".join([segment[:255] for segment in filename.split('/')])
        # 组合路径返回
        return os.path.join(self.cache_dir, filename)

    # 获取缓存数据
    def __getitem__(self, url):
        """以url为线索从磁盘获取数据"""
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                # 解压返回
                result, timestamp = pickle.loads(zlib.decompress(fp.read()))
                # 过期？
                if self.has_expired(timestamp):
                    raise KeyError(url + ' 数据过期')
                return result
        # 不存在文件则抛出异常
        else:
            raise KeyError(url + ' 文件不存在')

    # 设置缓存数据
    def __setitem__(self, url, result):
        """以url为线索向磁盘获存数据"""
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path, 'wb') as fp:
            # 记录时间戳
            timestamp = datetime.utcnow()
            data = pickle.dumps((result, timestamp))
            # 压缩存储
            fp.write(zlib.compress(data))

    # 判断时间是否过期
    def has_expired(self, timestamp):
        return datetime.utcnow() > timestamp + self.expires
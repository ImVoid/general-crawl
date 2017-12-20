# --coding:utf-8--

import re
import os
import urlparse
import pickle

class DiskCache:
    """利用文件系统缓存
    """
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir

    # 将url映射为文件路径
    def url_to_path(self, url):
        # 分割url的不同部分
        components = urlparse.urlparse(url)
        # 为空path & “/”结尾的url添加index.html后缀
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
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
                return pickle.load(fp)
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
            fp.write(pickle.dumps(result))

print DiskCache().url_to_path('http://example.webscraping.com/index?adb=a')
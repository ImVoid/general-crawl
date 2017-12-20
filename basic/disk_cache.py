# --coding:utf-8--

import re
import os
import urlparse

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

print DiskCache().url_to_path('http://example.webscraping.com/index?adb=a')
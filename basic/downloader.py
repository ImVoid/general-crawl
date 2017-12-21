# --coding:utf-8--

import urlparse
import datetime
import time
import random
import urllib2

DEFAULT_DELAY = 5
DEFAULT_AGENT = 'wswp'
DEFAULT_RETRIES = 1

class Downloader:
    """封装为类的页面下载器,通过将参数在构造函数中设置避免重复操作"""
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT,
                 proxies=None, num_retries=DEFAULT_RETRIES, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent=user_agent
        self.proxies=proxies
        self.num_retries=num_retries
        self.cache=cache

    def __call__(self, url):
        result = None
        # 如果启动了缓存，从缓存中取数据
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # 缓存中并无此Key
                pass
            # 无异常发生进入else模块，检查缓存结果的状态码是否5xx,是则将结果置为None触发重新下载
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    result = None

        # 没有从缓存中找到记录或者记录状态码为5xx的需要下载
        if result is None:
            # 限速
            self.throttle.wait(url)
            # 如果使用了ip代理
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent' : self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            # 存到缓存中
            if self.cache:
                self.cache[url] = result;
        return result['html']

    # 下载页面:
    # 错误检测
    # 服务端错误重试（默认两次）
    # 用户代理设置（默认wswp:web scraping with python）
    # http代理 proxy='202.96.142.2:3128'
    # 下载限速（秒）
    def download(self, url, headers, proxy=None, num_retries=2):
        print '下载页面:', url
        # 设置用户代理
        request = urllib2.Request(url, headers=headers)

        # 设置http代理
        opener = urllib2.build_opener()
        if proxy:
            # 为处理器准备参数
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            # 添加代理处理器
            opener.add_handler(urllib2.ProxyHandler(proxy_params))

        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        # 错误检测
        except Exception as e:
            print '下载失败：', e.reason
            html = ''
            if hasattr(e, 'code'):
                code = e.code

            # 下载重试
            # 当http代码是5xx的时候意味着服务端发生错误，重试下载时可能已经被修复
            if num_retries > 0 and 500 <= e.code < 600:
                    return download(url, headers, proxy, num_retries - 1)
        return {'html': html, 'code': code}

class Throttle:
    """下载限速：在两次访问相同的域名时，间隔指定秒数"""

    def __init__(self, delay):
        # 延迟的秒数
        self.delay = delay
        # 记录每个域名的最后访问时间戳
        self.domains = {}

    def wait(self, url):
        # 获取域名
        domain = urlparse.urlparse(url).netloc
        # 获取该域名最后访问时间戳
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            # 剩余延迟时间
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            # 若还未满足间隔
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        # 更新该域名最后访问时间
        self.domains[domain] = datetime.datetime.now()


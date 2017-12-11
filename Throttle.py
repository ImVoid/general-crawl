# --coding:utf-8--
import urlparse
import datetime
import time

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
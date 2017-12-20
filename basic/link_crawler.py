# --coding:utf-8--

# 链接爬虫
# 过滤重复链接
# 限定爬取深度，首页深度为1
# 限速
# 提供回调函数
import re
import urlparse
from downloader import Downloader

def link_crawler(seed_url, link_regex, delay=5, max_depth=2, user_agent='wswp', proxies=None,
                 num_retries=1, throttle=None, scrae_callback=None, cache=None):
    """从种子链接seed_url，爬取所有匹配正则的url"""
    crawl_queue = [seed_url]
    # 唯一的保存相同的链接&深度
    seen = {seed_url:0}
    D = Downloader(delay, user_agent, proxies, num_retries, cache)
    # 下载每个html页面
    while crawl_queue:
        url = crawl_queue.pop()
        html = D(url)

        # 调用回调函数
        if scrae_callback:
            scrae_callback(url, html)

        # 获取现页面的深度
        depth = seen[url]
        # 如果深度到达约定数，则不再爬取链接
        if depth != max_depth:
            # 将每个html页面符合条件的url加入队列
            for link in get_links(html):
                if re.search(link_regex, link):
                    # 补全链接
                    link = urlparse.urljoin(seed_url, link)
                    # 如果已经入队，则不必再入队，避免重复下载
                    if link not in seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)

def get_links(html):
    """返回一个页面的所有链接"""
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

filename = 'http://example.webscraping.com/index/'
url = 'http://example.webscraping.com/index?adb=a'

import urlparse
import os

print urlparse.urlsplit(url)
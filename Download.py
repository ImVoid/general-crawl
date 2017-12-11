# --coding:utf-8--
import urllib2

# 下载页面:
# 错误检测
# 服务端错误重试（默认两次）
# 用户代理设置（默认wswp:web scraping with python）
def download(url, user_agent='wswp', num_retries=2):
    print '下载页面:', url
    # 设置用户代理
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    try:
        html = urllib2.urlopen(request).read()
    # 错误检测
    except urllib2.URLError as e:
        print '下载失败：', e.reason
        html = None

    # 下载重试
        if num_retries > 0:
            # 当http代码是5xx的时候意味着服务端发生错误，重试下载时可能已经被修复
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries-1)
    return html


# 网站地图爬虫
import re
def crawl_sitemap(sitemap_url):
    # 下载网站地图xml
    sitemap = download(sitemap_url);
    # 从xml中的<loc>标签提取url
    links = re.findall('<loc>(.*?)</loc>', sitemap);
    # 遍历下载每个链接
    for link in links:
        html = download(link)
        # TODO 处理内容


# ID遍历爬虫
import itertools
# max_errors:连续多少个页面错误视为结束ID遍历
# num_errors:记录当前的页面错误数
def crawl_id(url_prefix, max_errors=5, num_errors=0):
    for num in itertools.count(1):
        full_url = url_prefix + '%d' % num
        html = download(full_url)
        if html is None:
            num_errors += 1;
            # 如果达到max_errors就结束遍历
            if num_errors == max_errors:
                break
        else:
            # 成功恢复
            num_errors = 0

# 链接爬虫
# 过滤重复链接
import re
import urlparse
def link_crawler(seed_url, link_regex):
    """从种子链接seed_url，爬取所有匹配正则的url"""
    crawl_queue = [seed_url]
    # 唯一的保存相同的链接
    seen = set(crawl_queue)
    # 下载每个html页面
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        # 将每个html页面符合条件的url加入队列
        for link in get_links(html):
            if re.search(link_regex, link):
                # 补全链接
                link = urlparse.urljoin(seed_url, link)
                # 如果已经入队，则不必再入队，避免重复下载
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

def get_links(html):
    """返回一个页面的所有链接"""
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

link_crawler('http://example.webscraping.com/', '/(index|view)')
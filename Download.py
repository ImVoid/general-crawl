# -*-coding:utf-8-*-
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

print download("http://www.baidu.com/")
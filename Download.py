# -*-coding:utf-8-*-
import urllib2

# 下载页面:
# 包含错误检测与服务端错误重试（默认两次）
def download(url, num_retries=2):
    print '下载页面:', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print '下载失败：', e.reason
        html = None
        # 检查是否重试下载
        if num_retries > 0:
            # 当http代码是5xx的时候意味着服务端发生错误，重试下载时可能已经被修复
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries-1)
    return html

print download("http://httpstat.us/500")